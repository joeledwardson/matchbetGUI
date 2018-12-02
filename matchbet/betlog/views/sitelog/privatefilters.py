from itertools import chain
from operator import attrgetter
import django_filters
from django.db.models import F, CharField, QuerySet

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
    filter_classes = {model: sitelog_filter_class(model) for model in models}

    # filter instances list
    filter_instances = {model: None for model in models}

    # filter used by template
    filter = None

    # queryset - set in get()
    qs = None

    # Site instance used in page
    site = None

    # assign default ordering
    order_default = order_default

    # get queryset of a model, filtered using field with name [siteFieldName] i.e. 'site' to [site] object
    def get_model_qs(self, model, site):

        # filter to site by the [site] object stored in class
        site_filter = {siteFieldName: site}

        # return filtered queryset to site object
        return model.objects.filter(**site_filter)


    # get django fitler instance queryset, filtered with parameters in [get]
    def get_filter_instance(self, GET_dict, model, site, Filter_class):

        # retrieve queryset filtered by site
        qs = self.get_model_qs(model, site)

        # create and return fitler instance
        # if objectType.name is in GET_dict, filter will use [field_name] to filter
        return Filter_class(GET_dict, queryset=qs)


    # annotate a queryset with a type field to objectType
    # e.g. queryset with 'transactionType__name' would be annotated to 'object_type'
    def annotate(self, qs, typeFieldName):

        # create annotation dictionary
        d = {objectType.name: F('{}__name'.format(typeFieldName))}

        # return annotated queryset
        return qs.annotate(**d)


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

# decorative function to call over get()
#   sets self.filter and self.qs
def filter_get(get):

    def inner(self: SiteLog_FilterView, request, *args, **kwargs):

        # create filter instances
        for model in models:
            self.filter_instances[model] = self.get_filter_instance(
                GET_dict=request.GET,
                model=model,
                site=self.site,
                Filter_class=self.filter_classes[model]
            )

        # annotate filter querysets so they have matching 'object_type' values
        qs_list = [
            self.annotate(
                self.filter_instances[model].qs,
                typeFields[model]
            ) for model in models
        ]

        # order querysets using order 'order_by' parameter, assign to class so can be read by get_table_qs()
        self.qs = self.order_querysets(
            qs_list,
            order_by=request.GET.get('order_by'))


        # use one of the filter_instances in list for filter instance used in template
        self.filter = next(iter(self.filter_instances.values()))

        return get(self, request, *args, **kwargs)

    return inner