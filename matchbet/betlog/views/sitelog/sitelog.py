from django.shortcuts import get_object_or_404, reverse

from betlog.models import Site, Transaction, Bet
from betlog.sessions import set_last_view
from betlog.views.table import table_view_class, table_getter, css_good_type, css_bad_type
from betlog.views.message import set_message
from betlog.names import model_name, viewname_app, model_viewname

from .privatefilters import SiteLog_FilterView
from .privateforms import SiteLog_FormView, models
from .globals import sitelog_view_name, sitelog_site_var, fields, objectType


# create table view from generic builer class with fields
table_view = table_view_class(fields, sitelog_view_name)

def get_site(pk):
    return get_object_or_404(Site, pk=pk)

# View class for viewing a specific site
class SiteLogView(SiteLog_FormView, SiteLog_FilterView, table_view):

    view_name = sitelog_view_name # need view name for url conf and table update links
    view_kwargs = None # hold site name - required

    template_name = 'sitelog.html' # custom template - does not use create form (is added by default)
    title = None # add friendly display title to context (otherwise will use Sitelog - not very nice to look at!

    # set queryset in get(), to be retrieved by get_table_qs when table is getting its queryset for context
    qs = None

    # override table get queryset function - return Transaction and Bet joined list
    def get_table_qs(self):

        return self.qs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # add transaction and bet models for forms
        context['form_data'] = [{
            'name': model_name(model),
            'form': self.forms[model],
            'url': reverse(viewname_app(model_viewname(model)))
        } for model in models]


        return context

    @table_getter
    @set_message
    @set_last_view
    def get(self, request, *args, **kwargs):

        # get site using pk from kwargs
        site = get_site(kwargs.get('pk'))

        # get filter instances
        filters = self.get_filter_instances(request.GET, site)

        # use one of the filter_instances in list for filter instance used in template
        self.filter = next(iter(filters.values()))

        # assign filters queryset to self, to be read by get_table_qs()
        self.qs = self.get_filters_queryset(filters, request.GET.get('order_by'))

        # assign forms to self using site
        self.forms = self.get_forms(site)

        # set view key word args - read by set_last_view_wrap
        self.view_kwargs = {sitelog_site_var: site.name, 'pk': site.pk}

        # set page title with site name
        self.title = '{} log'.format(site.name)

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
        'pk': '\d+',
        sitelog_site_var: r'[^/]+',
    }
}