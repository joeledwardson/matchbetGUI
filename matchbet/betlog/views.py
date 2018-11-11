from .mycommonview import create_common_view, create_update_vew
from .mysitelogview import sitelog_view_name, sitelog_site_var
from .models import Site, Match, Transaction, Bet
from .mytableview import css_bad_type, css_good_type
from .names import viewname_app
from .sessions import get_last_view, set_last_view

from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.utils.text import slugify

from itertools import chain

transaction_css_rules = [css_bad_type('transactionType', badVal='Fee')]

bet_css_rules = [css_good_type('betType', goodVal='Win'),
                 css_bad_type('betType', badVal='Loss')]



# Site views
view_site = create_common_view(Site)
# override object link (by default is update) to go to sitelog, add site name as url var
view_site.get_object_link = lambda self, site: reverse(
    viewname_app(sitelog_view_name),
    kwargs={
        'pk': site.pk,
        sitelog_site_var: slugify(site.name),
    })
views_site = {'default': view_site, 'update': create_update_vew(Site)}

# Match View
view_match = create_common_view(Match)
views_match = {'default': view_match, 'update': create_update_vew(Match)}

# Transaction view
view_transaction = create_common_view(Transaction)
view_transaction.css_rules = transaction_css_rules
views_transaction = {'default': view_transaction, 'update': create_update_vew(Transaction)}

# Bet view
view_bet = create_common_view(Bet)
view_bet.css_rules = bet_css_rules
views_bet = {'default': view_bet, 'update': create_update_vew(Bet)}

# default view
def default_view(request):
    return HttpResponseRedirect(reverse(viewname_app(view_site.view_name)))

# view classes - must put in order! used by default in navigation pane of template
view_classes = [views_site, views_transaction, views_bet, views_match]


# override get function
def get(self, request, *args, **kwargs):

    # get page response
    page = super(type(self), self).get(request, *args, **kwargs)

    # set current view for next page
    set_last_view(request, self.view_name)


    return page

# set get function for all default classes (not updates or last view will be overriden!)
for view_dict in view_classes:
    view_dict['default'].get = get