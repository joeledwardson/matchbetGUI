from django.urls import path, re_path

from .apps import BetlogConfig
from .names import _append_success
from .views.views import view_classes
from betlog.views.sitelog.sitelog import sitelog_view_dict

from djmoney.admin import setup_admin_integration
setup_admin_integration()

app_name = BetlogConfig.name

def path_constructor(view):
    default = 'default'
    update = 'update'
    url_vars = 'url_vars'

    name = view[default].view_name
    mk_url_vars = lambda url_vars: ''.join(r'<{}:{}>/'.format(url_vars[v], v) for v in url_vars)
    get_url_vars = lambda view: mk_url_vars(view[url_vars] if url_vars in view else r'')

    path_list = [
        path('{}/{}'.format(name, get_url_vars(view)),
             view=view[default].as_view(log_status=0),
             name=name),

        path('{}/success/{}'.format(name, get_url_vars(view)),
             view=view[default].as_view(log_status=1),
             name=_append_success(name,True)),

        path('{}/failure/{}'.format(name, get_url_vars(view)),
             view=view[default].as_view(log_status=2),
             name=_append_success(name, False))]

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
