from betlog.names import viewname_app
from betlog.models import Site, Match, Transaction, Bet

from .update import update_view_class
from .common import create_common_view
from .sitelog.globals import sitelog_view_name, sitelog_site_var
from .table import css_bad_type, css_good_type

from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.utils.text import slugify

transaction_css_rules = [css_bad_type('transactionType', badVal='Fee')]

bet_css_rules = [css_good_type('betType', goodVal='Win'),
                 css_bad_type('betType', badVal='Loss')]

model_views = lambda model: {
    'default': create_common_view(model),
    'update': update_view_class(model),
}


# Site views
views_site = model_views(Site)
# override object link (by default is update) to go to sitelog, add site name as url var
views_site['default'].get_object_link = lambda self, site: reverse(
    viewname_app(sitelog_view_name),
    kwargs={
        'pk': site.pk,
        sitelog_site_var: slugify(site.name),
    })
# dont allow deleting of sites - must be done in admin
views_site['update'].allow_delete = False

# Match View
views_match = model_views(Match)


# Transaction view
views_transaction = model_views(Transaction)
views_transaction['default'].set_css_rules(transaction_css_rules)


# Bet view
views_bet = model_views(Bet)
views_bet['default'].set_css_rules(bet_css_rules)


# default view - site list
def default_view(request):
    return HttpResponseRedirect(reverse(viewname_app(views_site['default'].view_name)))


# view classes - must put in order! used by default in navigation pane of template
view_classes = [views_site, views_transaction, views_bet, views_match]