from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.db.models import CharField
from itertools import chain
from operator import attrgetter
import django_filters

from .models import Transaction, Bet, fieldnames_all, fields_all, Site, TransactionType, BetType
from .filters import create_filter
from .mytableview import table_view_class, css_good_type, css_bad_type
from .mylogview import LogView
from .sessions import set_last_view
from .filters import MySelectorWidget
from .filters import SliderWidget

# custom view name - normally based on model
sitelog_view_name = 'sitelog'
# variable name which holds site name - used in url configuration
sitelog_site_var = 'viewsite'


transactionTypeField = 'transactionType'  # transaction 'type' foreign key field name
betTypeField = 'betType'  # bet 'type' foreign key field name
siteFieldName = 'site'  # site foreign key field name for transaction/bet

# create values for filter
type_values = lambda type_model: [
    (v.name, v.name) for v in type_model._default_manager.all()
]

# object 'type' field - concatenates transaction type and bet type
objectType = CharField(
    max_length=255,
    blank=True,
    name='object_type', # must use one of the field types to get filter to print 'Type'
    verbose_name='Type',
    choices=[
        ['Transaction', tuple(type_values(TransactionType))],
        ['Bet', tuple(type_values(BetType))]
    ]
)


# first field is object 'type'
fields = [objectType]

# get all fields common between Bet and Transaction - (filter to specific site)
fields += [
    f for f in fields_all(Transaction)
    if f.name in fieldnames_all(Bet) and
    f.related_model is not Site
]

# create table view
table_view = table_view_class(fields, sitelog_view_name)

type_name = lambda type_field: '{}__name'.format(type_field)

create_sitelog_filter = lambda typeFieldName: create_filter(fields, sitelog_view_name, {
    objectType.name: django_filters.ChoiceFilter(
        label='Type',
        field_name=type_name(typeFieldName),
        choices=objectType.choices,
        widget=MySelectorWidget
    ),
})

class SiteLogView(table_view, LogView):

    view_name = sitelog_view_name # need view name for url conf and table update links
    view_kwargs = None # hold site name - required
    template_name = 'sitelog.html' # custom template - does not use create form (is added by default)
    title = None # add friendly display title to context (otherwise will use Sitelog - not very nice to look at!
    site_name = None # name of site to set in get function

    # transaction filter class
    Filter_transaction = create_sitelog_filter(transactionTypeField)
    # bet filter class
    Filter_bet = create_sitelog_filter(betTypeField)

    # override table get queryset function - return Transaction and Bet joined list
    def get_table_qs(self):

        return self.qs

    def get_context_data(self, **kwargs):

        # assign log context data
        self.get_log_context_data()

        # assign table context data
        self.get_table_context_data()

        # get template context data
        context = super().get_context_data(**kwargs)

        return context


    # get queryset of a model, filtered using field with name [siteFieldName] i.e. 'site' to [site] object
    def get_qs(self, model, site):

        # filter to site by the [site] object stored in class
        site_filter = {siteFieldName: site}

        # return filtered queryset to site object
        return model.objects.filter(**site_filter)


    # get django fitler instance queryset, filtered with parameters in [get]
    def get_filter_instance(self, GET_dict, model, site, Filter_class):

        # retrieve queryset filtered by site
        qs = self.get_qs(model, site)

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
    def order_querysets(self, qs_list, order_by, order_default):

        # if order by parameter is empty, use default order by
        if not order_by:
            order_by = order_default

        # '-' indicates reversed, however database are printed top to bottom so invert boolean
        order_reversed = not(order_by.startswith('-'))

        # remove '-', then can use getattr() to retrieve field
        order_by = order_by.strip('-')

        # sort list of pointers to querysets, using getattr of [order_by] parameter
        return sorted(
            chain(*qs_list),
            key=attrgetter(order_by),
            reverse=order_reversed
        )

    @set_last_view
    def get(self, request, *args, **kwargs):

        # get site from GET in url
        site = get_object_or_404(Site, pk=kwargs.get('pk'))
        # assign to self
        self.site = site

        # set view key word args - read by set_last_view_wrap
        self.view_kwargs = {sitelog_site_var: site.name, 'pk': site.pk}

        # set page title with site name
        self.title = '{} log'.format(site.name)

        # create transaction and bet filter instances
        filter_transaction = self.get_filter_instance(request.GET, Transaction, site, self.Filter_transaction)
        filter_bet = self.get_filter_instance(request.GET, Bet, site, self.Filter_bet)

        # annotate filter querysets so they have matching 'object_type' values
        qs_list = [self.annotate(filter_transaction.qs, transactionTypeField),
                   self.annotate(filter_bet.qs, betTypeField)]

        # order querysets using order 'o' parameter, assign to class so can be read by get_table_qs()
        self.qs = self.order_querysets(qs_list, order_by=request.GET.get('o'), order_default='date')

        # assign transaction filter to class value for reading by template (choice between transaction/bet is arbitrary)
        self.filter = filter_transaction

        return super().get(request, *args, **kwargs)

    # use rules for transaction and bet - type field is string type
    css_rules = [
        css_bad_type(objectType.name, badVal='Fee', field_val_getter=str),
        css_good_type(objectType.name, goodVal='Win', field_val_getter=str),
        css_bad_type(objectType.name, badVal='Loss', field_val_getter=str)]

# view dictionary for url to read
#   key - name of variable in url
#   value - type
sitelog_view_dict = {
    'default': SiteLogView,
    'url_vars': {
        'pk': 'int',
        sitelog_site_var: 'str',
    }
}