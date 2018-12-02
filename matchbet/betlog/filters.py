import itertools

import django_filters
from django_filters import widgets as filter_widgets
from django.forms import widgets
from django.db import models

from .widgets import MySelectorWidget, MySelectorWidget_NoClear, css_date_class, FriendlyBooleanWidget
from .names import numeric_fields, date_fields


# list of filter dicts
#   key - name of filter you want to manually refer to it
#   value (dict)
#       fields - model fields to match against
#       filter - filter to create
#       widget - widget to create
#       widget_attrs - widget attrs
filters = {
    'selector': {
        'fields': [models.ForeignKey],
        'filter': django_filters.ChoiceFilter,
        'widget': MySelectorWidget
    },
    'date': {
        'fields': [models.DateField, models.DateTimeField],
        'filter': django_filters.DateFromToRangeFilter,
        'widget': filter_widgets.RangeWidget,
        'widget_attrs': {'class': css_date_class},
    },
    'boolean': {
        'fields': [models.BooleanField],
        'filter': django_filters.BooleanFilter,
        'widget': FriendlyBooleanWidget,
    },
    'numeric': {
        'fields': numeric_fields,
        'filter': django_filters.NumericRangeFilter,
        'widget': filter_widgets.RangeWidget,
    }
}


# Order class - used to order a queryset
class Orderer:

    # get order key - simply gets a name from object field end pre-pends with - if invert is True
    @classmethod
    def order_key(cls, field_name, invert=False):
        inv = lambda s: '-{}'.format(s)
        return inv(field_name) if invert else field_name

    # get order label - formats a field name with a remark string
    @classmethod
    def order_label(cls, field, remark):
        return '{name}: {remark}'.format(
            name=field.verbose_name.capitalize(),
            remark=remark
        )

    # generate a tuple-pair of order [key, label] - use positive = False to invert direction
    @classmethod
    def choice(cls, field, remark, positive=True):
        return tuple((
            cls.order_key(field.name, positive),
            cls.order_label(field, remark)
        ))

    # generate choice tuple pairs
    #   "Date" like fields - newest/oldest first
    #   "Numeric" like fields - largest/smallest first
    #   "Character" like fields - acesnding/descending
    @classmethod
    def get_ordering_choices(cls, model_fields):

        char_fields = (models.CharField,)

        order_strings = {
            date_fields: [
                lambda f: cls.choice(f, 'Newest First', True),
                lambda f: cls.choice(f, 'Oldest First', False)
            ],
            numeric_fields: [
                lambda f: cls.choice(f, 'Largest First', True),
                lambda f: cls.choice(f, 'Smallest First', False)
            ],
            char_fields: [
                lambda f: cls.choice(f, 'Acsending', True),
                lambda f: cls.choice(f, 'Descending', False)
            ]
        }

        order_choices = []

        for f in model_fields:
            for o in order_strings:
                if type(f) in o:
                    order_choices += [s(f) for s in order_strings[o]]
                    break

        return order_choices

    # get ordering filter and order invert filter - return dictionary of filter_instances and methods
    @classmethod
    def get_order_filter(cls, model_fields):

        # create ordering filter
        return django_filters.OrderingFilter(
            choices=cls.get_ordering_choices(model_fields),
            widget=MySelectorWidget_NoClear,
            label='Order by',
        )


# create filter instance from field
#   field: django form field
#   cls_name: TODO replace with ID incrementor
#   filter_class: filter to create instance of
#   widget_class: optional widget class
#   widget_attrs: optional attrs to pass when creating widget
def get_filter(field, cls_name, filter_class, widget_class, widget_attrs) -> django_filters.Filter:

    # create filter dictionary, start with  field name
    filter_dict = {'field_name': field.name}

    # if type is foreignkey, add queryset so model choice can populate choices
    if type(field) == models.ForeignKey:
        filter_dict['choices'] = field.get_choices()

    # if widget filter then create (otherwise will be created implicitly)
    if widget_class:

        # get widget attributes if specified
        widget_attrs = widget_attrs or {}

        # assign custom HTML id so no confusion between filter form and other forms
        widget_attrs['id'] = 'id_{}_{}'.format(cls_name, field.name)

        # create widget and place in filter dictionary
        filter_dict['widget'] = widget_class(attrs=widget_attrs)

    # create filter instance itself
    return filter_class(**filter_dict)


# get dictionary of field names to [fitlers] element containing 'filter' key
def get_field_filters(model_fields):

    # map model fields to filter if filter is required
    field_filters = {}

    # loop fields
    for field in model_fields:

        try:

            # get first filter_instances element if type of field matches any of the field types in 'fields' element
            f = next(
                {field: filters[filt]}
                for filt in filters
                if type(field) in filters[filt]['fields']
            )

            # update dictionary
            field_filters.update(f)

        except StopIteration:

            # if no match catch exception thrown by next()
            pass

    return field_filters


# Custom filter set class
class GenericFilterSet(django_filters.FilterSet):

    order_default = None

    # set order_by default values on instance creation, unless passed in data
    def __init__(self, data=None, queryset=None, **kwargs):

        # if empty create data dict - if not must copy as it's immutable
        data = data.copy() or {}

        # check if ordering parameter passed
        if not data.get('order_by'):

            # ordering parameter not passed, use default
            data['order_by'] = self.order_default

        # run filter set initialisation
        django_filters.FilterSet.__init__(self, data, queryset, **kwargs)


# create filter class based on model
#   model_fields - list of fields, filter_instances will be created upon type
#   view_name - name to use when creating class
#   custom_fields - dict of custom field filter_instances
#   order_default - order by parameter - can generate using Orderer.order_key
def create_filter_set(model_fields, view_name, *, custom_fields=None, order_default=None) -> GenericFilterSet:

    print('--> Creating filter...\nfields: {}\nview name: {}, custom fields: {}\n'.format(
        model_fields,
        view_name,
        custom_fields
    ))

    # first set name of class to create
    cls_name = 'Filter{}'.format(view_name)

    # create class dictionary - intial values are custom field filter_instances
    cls_dict = custom_fields or {}

    # get dictionary of fields to their filter dict elements
    field_filters = get_field_filters(model_fields)

    # loop fields
    for field in field_filters:

        # get associated field filter dict
        filter_elements = field_filters[field]

        # get filter class, widget (optional) and widget attributes (optional)
        [filter_class, widget_class, widget_attrs] = [
            filter_elements['filter'],
            filter_elements.get('widget'),
            filter_elements.get('widget_attrs')
        ]

        # create filter instance itself and add to class dictionary
        cls_dict[field.name] = get_filter(field, cls_name, filter_class, widget_class, widget_attrs)

    # set default order
    cls_dict['order_default'] = order_default

    # add ordering filter
    cls_dict['order_by'] = Orderer.get_order_filter(model_fields)

    # create class type
    return type(cls_name, (GenericFilterSet, ), cls_dict)


