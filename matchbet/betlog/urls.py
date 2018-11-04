from django.urls import path, re_path

from .apps import BetlogConfig
from .names import _append_success
from .views import view_classes
from .mysitelogview import sitelog_view_dict


app_name = BetlogConfig.name

def path_constructor(view):
    default = 'default'
    update = 'update'
    url_vars = 'url_vars'

    name = view[default].view_name
    mk_url_vars = lambda url_vars: ''.join('<{}:{}>/'.format(v['type'], v['name']) for v in url_vars)
    get_url_vars = lambda view: mk_url_vars(view[url_vars] if url_vars in view else '')

    path_list =  [
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
        updateName = view[update].view_name

        match_str = r'^{name}/update/id-(?P<pk>\d+)/$'.format(name=name)

        path_list.append(re_path(
            match_str,
            view=view[update].as_view(),
            name=updateName))

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

# urlpatterns.append(path('test/', SiteLogView.as_view(), name=SiteLogView.view_name))
# urlpatterns.append(path('index/', DefaultView.as_view(), name='index'))
# urlpatterns.append(path('test/', TestView.as_view(), name=TestView.view_name))
# urlpatterns.append(path('test/update/<pk>/', TestView.as_view(), name=append_update(TestView.view_name)))