from itertools import chain
from operator import attrgetter
import django_filters
from django.db.models import F, CharField, QuerySet

from betlog.models import Site
from betlog.filters import create_filter_set, Orderer
from betlog.widgets import MySelectorWidget
from .globals import sitelog_view_name, siteFieldName, models, objectType, fields, typeFields


# by default - order by date, want newest first so invert
order_default = Orderer.order_key('date', invert=True)

# func to access ModelType.name in a query
type_name = lambda type_field: '{}__name'.format(type_field)


# func to create filter class (need 2 for Bet and Transaction)
def sitelog_filter_class(typeFieldName):

    # custom choice filter for Bet/Transaction Type
    typeFilter = django_filters.ChoiceFilter(
        label='Type',
        field_name=type_name(typeFieldName),
        choices=objectType.choices,
        widget=MySelectorWidget
    )

    # create filter class with custom filter
    # e.g. a filter under the name 'object_type' will be set to 'transactionType__name' for Transactions
    return create_filter_set(
        fields,
        sitelog_view_name,
        order_default=order_default,
        custom_fields= {
            objectType.name: typeFilter,
        }
    )

class SiteLog_FilterView:

    # filter classes list
    filter_classes = {model: sitelog_filter_class(typeFields[model]) for model in models}

    # assign default ordering
    order_default = order_default

    # retrieve filter instances
    def get_filter_instances(self, get_dict: dict, site: Site):

        # create empty dict
        filters = {}

        # filter to site by the [site] object stored in class
        site_filter = {siteFieldName: site}

        # loop models
        for model in models:

            # retrieve model queryset filtered by site
            qs = model.objects.filter(**site_filter)

            # add filter instance via model key using GET dictionary and queryset
            filters[model] = self.filter_classes[model](get_dict, queryset=qs)

        # return filters dictionary
        return filters

    # join queryset list together and order them
    def order_querysets(self, qs_list, order_by):

        # check if order_by paramter is None if order by parameter is empty, use default order by
        if not order_by:
            # use default ordering
            order_by = self.order_default

        # '-' indicates reversed, however database are printed top to bottom so invert boolean
        order_reversed = order_by.startswith('-')

        # remove '-', then can use getattr() to retrieve field
        order_by = order_by.strip('-')

        # sort list of pointers to querysets, using getattr of [order_by] parameter
        return sorted(
            chain(*qs_list),
            key=attrgetter(order_by),
            reverse=order_reversed
        )

    # get ordered query set from filters dict using [order_by] arg, if blank self.default_order will be used
    def get_filters_queryset(self, filters, order_by):

        # create empty queryset list
        qs_list = []

        # loop models
        for model in models:

            # get type field (e.g. transcationType)
            type_field = typeFields[model]

            # create annotation dictionary, 'transactionType__name' would be annotated to 'object_type'
            d = {objectType.name: F('{}__name'.format(type_field))}

            # get annotated queryset from model filter
            qs_annotated = filters[model].qs.annotate(**d)

            # add annotated filter qs to list
            qs_list.append(qs_annotated)

        return self.order_querysets(qs_list, order_by)

