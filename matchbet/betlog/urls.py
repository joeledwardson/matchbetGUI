from django.urls import path, re_path

from .apps import BetlogConfig
from .views.views import view_classes
from betlog.views.sitelog.sitelog import sitelog_view_dict

from djmoney.admin import setup_admin_integration
setup_admin_integration()

app_name = BetlogConfig.name

# construct url patterns for a model. [view] input is a dictionary, which should contain:
#   'default' - a default view, accepting message_var indicating success or failure of an operation
#   'update' [optional] - an update view
#   'url_vars' - a dictionary of [parameter name: regular expression matching string]
def path_constructor(view):
    default = 'default'
    update = 'update'
    url_vars = 'url_vars'

    # name of view
    name = view[default].view_name

    # make url string from url variables, e.g. for url_vars={'somenumber': r'\d+'} it would make 'somenumber:\d+>/'
    mk_url_vars = lambda url_vars: ''.join(r'(?P<{var}>{restr})/'.format(var=v, restr=url_vars[v]) for v in url_vars)

    # get url variables from view dictionary, and return empty string if url_vars does not exist
    get_url_vars = lambda view: mk_url_vars(view[url_vars] if url_vars in view else r'')

    # re expression for message update
    re_msg = r'(?:update_success=(?P<message_var>True|False)/)?'

    # re expression for page numbering
    re_page = r'(?:page=(?P<pg_num>\d+)/)?'

    path_list = [
        re_path(r'^{}/{}{}{}$'.format(name, get_url_vars(view), re_msg, re_page),
             view=view[default].as_view(),
             name=name)
    ]

    if update in view:

        update_view_name = view[update].view_name

        match_str = r'^{view_name}/update/id-(?P<pk>\d+)/$'.format(view_name=name)

        path_list.append(re_path(
            match_str,
            view=view[update].as_view(),
            name=update_view_name
        ))

    return path_list

# path()
#   1st argument (positional) =  route - actual www address
#   2nd argument (positional) = view - function to call to return view
#   [kwargs] - keyword arguments
#   [name] - name to use when refering to view. In betlog app so for index is 'betlog:index'
# ^....$ means string must match exactly - cannot have extra trailing or leading characterse
# /? specifies optional forward slash
urlpatterns = [p for v in view_classes for p in path_constructor(v)]
urlpatterns += path_constructor(sitelog_view_dict)
