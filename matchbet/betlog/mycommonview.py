from .mycreateview import create_view_class
from .myfilterview import filter_view_class
from .mylogview import LogView
from .myupdateview import update_view_class
from .mytableview import table_view_class, TableView
from .models import fieldnames_all, fields_all
from .names import model_viewname, model_update_viewname

from django.views.generic import CreateView

# default query set is order by date
def get_queryset_date(self):

    qs = super(type(self), self).get_queryset()

    return qs.order_by('-date')


# Need to call individual context data assignments
def get_context_data(self, **attrs):

    self.object = None

    # return create view context
    context =  CreateView.get_context_data(self, **attrs)

    # get table view context
    TableView.get_table_context_data(self)

    # get log view context
    LogView.get_log_context_data(self)

    return context

# Get filter's queryset data
def get_filter_qs(self):
    return self.filter.qs


# create generic view - has a create view [form], filter embedded in [filter] and log. If date field exists than orders
# by newest first
def create_common_view(model):

    # view name is the django name to refer to the view - appended with update to edit an existing object
    view_name = model_viewname(model)
    fields = fields_all(model)

    # view for creating new model - ALSO defines get_queryset() for filter view
    create_view = create_view_class(model, view_name)

    # filter view - adds 'filter' to view context
    filter_view = filter_view_class(fields, view_name)

    # table class - adds table values to view context
    table_view = table_view_class(fields, view_name)

    # log view - adds 'log' to context - success/fail info set on as_view(log_status) call

    class_dict = {
        'template_name': 'default.html',
        'get_context_data': get_context_data,
        'get_table_qs': get_filter_qs,
    }

    # if date field exists then by default order by date
    if 'date' in fieldnames_all(model):
        class_dict.update({'get_queryset': get_queryset_date})

    return type(view_name, (create_view, filter_view, table_view, LogView), class_dict)


# create update view for a specific model
def create_update_vew(model):

    # view name is required as the redirect upon successful editing of an object
    view_name = model_update_viewname(model)

    # create update view class
    return update_view_class(model, view_name)