from django.views.generic.base import TemplateView
from django.db.models import F
from itertools import chain
from operator import attrgetter

from .models import Transaction, Bet, fieldnames_all, fields_all, Site
from .names import get_field_name
from .filters import create_filter
from .mytableview import table_view_class, css_good_type, css_bad_type
from .mylogview import LogView
from .sessions import set_last_view

from django.db.models import QuerySet

# custom view name - normally based on model
sitelog_view_name = 'sitelog'
# variable name which holds site name - used in url configuration
sitelog_site_var = 'view_site'

# field name to hold Transaction and Bet type
typeField = 'typeName'

# get all fields common between Bet and Transaction - (filter to specific site)
commonFields = [f for f in fields_all(Transaction)
                if f.name in fieldnames_all(Bet) and
                f.related_model is not Site]

# create table view
table_view = table_view_class(commonFields, sitelog_view_name)

# add at begining of table field name list object type - will not be in commonFields as 'transactionType' and 'betType' are different
table_view._field_names.insert(0, typeField)

# add frienly view name for table titles
table_view.field_titles.insert(0, 'Type')

# fields containing a forign key to ModelType - defines the 'type' of object
transactionTypeField = 'transactionType'
betTypeField = 'betType'

# field containing site foreign key for Transaction and Bet
siteField = 'site'

class SiteLogView(table_view, LogView):

    view_name = sitelog_view_name # need view name for url conf and table update links
    view_kwargs = None # hold site name - required
    template_name = 'sitelog.html' # custom template - does not use create form (is added by default)
    title = None # add friendly display title to context (otherwise will use Sitelog - not very nice to look at!
    site_name = None # name of site to set in get function

    # override table get queryset function - return Transaction and Bet joined list
    def get_table_qs(self):

        # filter to site by its name
        site_filter = {'{}__name'.format(siteField): self.site_name}


        # transaction annotation query
        query_t = {typeField: F('{}__name'.format(transactionTypeField))}

        # filter transactions by site name
        filtered_t = Transaction._default_manager.filter(**site_filter)

        # transaction annotated queryset
        qs_t = filtered_t.annotate(**query_t)


        # bet annotation query
        query_b = {typeField: F('{}__name'.format(betTypeField))}

        # filter bets by site name
        filtered_b = Bet._default_manager.filter(**site_filter)

        # bet annotated queryset
        qs_b = filtered_b.annotate(**query_b)


        # join queryset together and order by date (inverted so newest first)
        return sorted(
            chain(qs_t, qs_b),
            key=attrgetter('date'),
            reverse=True
        )

    def get_context_data(self, **kwargs):

        # assign log context data
        self.get_log_context_data()

        # assign table context data
        self.get_table_context_data()

        # get template context data
        context = super().get_context_data(**kwargs)

        return context

    def get(self, request, *args, **kwargs):

        # get site name from GET in url
        self.site_name = kwargs.get(sitelog_site_var)

        # set page title with site name
        self.title = '{} Log'.format(self.site_name)

        # update view name history
        set_last_view(request, self.view_name, {sitelog_site_var:self.site_name})

        return super().get(request, *args, **kwargs)

    # use rules for transaction and bet - type field is string type
    css_rules = [
        css_bad_type(typeField, badVal='Fee', field_val_getter=str),
        css_good_type(typeField, goodVal='Win', field_val_getter=str),
        css_bad_type(typeField, badVal='Loss', field_val_getter=str)]

# view dictionary for url to read
sitelog_view_dict = {
    'default': SiteLogView,
    'url_vars': [{
        'type': 'str',
        'name': sitelog_site_var
    }]
}