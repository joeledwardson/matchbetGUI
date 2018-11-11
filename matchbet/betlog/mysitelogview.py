from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.db.models import CharField
from django.db.models import QuerySet
from itertools import chain
from operator import attrgetter
import django_filters

from .models import Transaction, Bet, fieldnames_all, fields_all, Site, TransactionType, BetType
from .names import get_field_name
from .filters import create_filter
from .mytableview import table_view_class, css_good_type, css_bad_type
from .mylogview import LogView
from .sessions import set_last_view
from .filters import MySelectorWidget

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


# filter class - add custom field for object type
sitelog_filter = create_filter(fields, sitelog_view_name, {
    transactionTypeField: django_filters.ChoiceFilter(
        choices=objectType.choices,
        widget=MySelectorWidget)
})


class SiteLogView(table_view, LogView):

    view_name = sitelog_view_name # need view name for url conf and table update links
    view_kwargs = None # hold site name - required
    template_name = 'sitelog.html' # custom template - does not use create form (is added by default)
    title = None # add friendly display title to context (otherwise will use Sitelog - not very nice to look at!
    site_name = None # name of site to set in get function
    filter_class = sitelog_filter

    # override table get queryset function - return Transaction and Bet joined list
    def get_table_qs(self):

        # # filter to site by its name
        # site_filter = {siteFieldName: self.site}
        #
        # # transaction annotation query
        # query_t = {objectType.name: F('{}__name'.format(transactionTypeField))}
        #
        # # filter transactions by site name
        # filtered_t = Transaction._default_manager.filter(**site_filter)
        # #
        # # # transaction annotated queryset
        # # qs_t = filtered_t.annotate(**query_t)
        # #
        # # qs_t = self.filter_class(get,
        # #                          queryset=Transaction._default_manager.filter(**site_filter))
        #
        # # bet annotation query
        # query_b = {objectType.name: F('{}__name'.format(betTypeField))}
        #
        # # filter bets by site name
        # filtered_b = Bet._default_manager.filter(**site_filter)
        #
        # print(filtered_b)
        #
        # # bet annotated queryset
        # qs_b = filtered_b.annotate(**query_b)
        #
        #
        # # join queryset together and order by date (inverted so newest first)
        # return sorted(
        #     chain(qs_t, qs_b),
        #     key=attrgetter('date'),
        #     reverse=True
        # )
        return self.qs

    def get_context_data(self, **kwargs):

        # assign log context data
        self.get_log_context_data()

        # assign table context data
        self.get_table_context_data()

        # get template context data
        context = super().get_context_data(**kwargs)

        return context

    def get(self, request, *args, **kwargs):

        # get site from GET in url
        site = get_object_or_404(Site, pk=kwargs.get('pk'))
        # assign to self
        self.site = site

        # set view key word args
        self.view_kwargs = {sitelog_site_var: site.name, 'pk': site.pk}

        # set page title with site name
        self.title = '{} log'.format(site.name)

        # filter to site by its name
        site_filter = {siteFieldName: self.site}

        get_dict = request.GET.copy()

        type_name = lambda type_field: '{}__name'.format(type_field)

        qs_t = Transaction.objects.filter(**site_filter)
        qs_b = Bet.objects.filter(**site_filter)

        # copy transaction type to bet type for filtering
        t = get_dict.get(transactionTypeField)
        if t:
            filter_dict = {type_name(transactionTypeField): t}
            qs_t = qs_t.filter(**filter_dict)

            filter_dict = {type_name(betTypeField): t}
            qs_b = qs_b.filter(**filter_dict)

            get_dict.pop(transactionTypeField)

        def get_filter(qs):
            return self.filter_class(get_dict,
                                     queryset=qs)

        filter_transaction = get_filter(qs_t)
        filter_bet = get_filter(qs_b)

        def annotate(qs, type_field):
            # qs = model._default_manager.filter(**site_filter)
            annotation = {objectType.name: F('{}__name'.format(type_field))}
            return qs.annotate(**annotation)

        # qs_t = filter_transaction.qs
        qs_t = annotate(filter_transaction.qs, transactionTypeField)
        qs_b = annotate(filter_bet.qs, betTypeField)

        order_by = get_dict.get('o') or 'date'
        # if order_by:
        #     order_reversed = not(order_by.startswith('-'))
        #     order_by.strip('-')
        # else:
        #     order_reversed = True
        #     order_by = 'date'

        # join queryset together and order by date (inverted so newest first)
        self.qs = sorted(
            chain(qs_t, qs_b),
            key=attrgetter(order_by),
            reverse=True
        )

        self.filter = filter_transaction

        # update view name history
        set_last_view(request, self.view_name, self.view_kwargs)

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