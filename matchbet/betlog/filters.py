import django_filters
from django_filters import widgets as filter_widgets
from django.forms import widgets
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

from .names import css_date_class, numeric_fields, css_select_class

# by default no select boolean widget displays 'Uknown' - use blank text for no selection
class FriendlyBooleanWidget(filter_widgets.BooleanWidget):
    def __init__(self, attrs):
        choices = (('', _('')),
                   ('true', _('Yes')),
                   ('false', _('No')))

        # skip BooleanWidget init and go straight to Choice widget super - override choices
        return forms.Select.__init__(self, attrs=attrs, choices=choices)


# list of filter dicts
#   name - name of filter you want to manually refer to it
#   fields - model fields to match against
#   filter - filter to create
#   widget - widget to create
#   attrs - widget attrs
filters = {
    'model_selector': {
        'fields': [models.ForeignKey],
        'filter': django_filters.ModelChoiceFilter,
        'widget': widgets.Select,
        'widget_attrs': {'class': css_select_class},
    },
    'selector': {
        'fields': [], # must pick this manually
        'filter': django_filters.ChoiceFilter,
        'widget': widgets.Select,
        'widget_attrs': {'class': css_select_class},
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


# create filter class based on model
def create_filter(model_fields, model_name):

    # first set name of class to create
    cls_name = 'Filter_{}'.format(model_name)

    # create dictionary to store class variables
    cls_dict = {}

    # map model fields to filter if filter is required
    fields = {
        field:filters[filt]
        for field in model_fields
        for filt in filters
        if type(field) in filters[filt]['fields']
    }

    # loop fields
    for f in fields:
        # get associated field filter
        form_filter = fields[f]

        # create filter dictionary, add field name
        filter_dict = {}
        filter_dict['field_name'] = f.name

        # if type is foreignkey, add queryset so model choice can populate choices
        if type(f) == models.ForeignKey:
            filter_dict['queryset'] = type(f.related_model())._default_manager.all()


        # if widget filter then create (otherwise will be created implicitly)
        widget_class = form_filter.get('widget')
        if widget_class:
            # get widget attributes if specified
            widget_attrs = form_filter.get('widget_attrs') or {}
            # assign custom HTML id so no confusion between filter form and other forms
            widget_attrs['id'] = 'id_{}_{}'.format(cls_name, f.name)
            # create widget and place in filter dictionary
            filter_dict['widget'] = widget_class(attrs=widget_attrs)

        # create filter instance itself and add to class dictionary
        cls_dict[f.name] = form_filter['filter'](**filter_dict)

    class MySelectorWidget(widgets.Select):
        def __init__(self):
            super().__init__(attrs={'class': css_select_class})


    cls_dict['o'] = django_filters.OrderingFilter(
        fields=list(
            (f.name, f.verbose_name) for f in model_fields
        ),
        widget=MySelectorWidget,
        label='Order by'
    )

    # create class type
    return type(cls_name, (django_filters.FilterSet,), cls_dict)


