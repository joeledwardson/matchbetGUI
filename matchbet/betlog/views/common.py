from betlog.views.create import create_view_class, CommonCreateView, CreateView
from betlog.views.filterview import filter_view_class, filter_get, FilterView
from betlog.views.log import LogView, get_log_context_data
from betlog.views.update import update_view_class, CommonUpdateView
from betlog.views.table import table_view_class, TableView, get_table_context_data

from betlog.models import fields_all
from betlog.names import model_viewname, model_update_viewname
from betlog.sessions import set_last_view

class CommonView(CommonCreateView, TableView, LogView, FilterView):

    template_name = 'default.html'

    # Need to call individual context data assignments
    @get_log_context_data # adds log to context
    @get_table_context_data # sets self.table_list
    def get_context_data(self, **attrs):

        # need to set object to None of getobject from CreateView gets unhappy?
        # self.object = None

        # return create view context
        context = super(CreateView, self).get_context_data(**attrs)

        # add model to context
        context['model'] = self.model
        # add current url to context
        context['my_url'] = self.request.path

        return context

    # custom get queryset method for TableView - use filtered queryset
    def get_table_qs(self):

        return self.filter.qs

    # explicitly override FilterView's not implemented get_queryset()
    def get_queryset(self):

        return CommonCreateView.get_queryset(self)

    # decorate with filter's get() to set self.filter
    @set_last_view
    @filter_get
    def get(self, request, *args, **kwargs):

        # return CreateView().get
        response = CreateView.get(self, request, *args, **kwargs)

        return response

# create generic view - has a create view [form], filter embedded in [filter] and log. If date field exists than orders
# by newest first
def create_common_view(model) -> CommonView:

    print('Creating common view based on model "{}"'.format(model))

    # view name is the django name to refer to the view - appended with update to edit an existing object
    view_name = model_viewname(model)
    fields = fields_all(model)

    view_classes = (
        CommonView,
        create_view_class(model, view_name), # create view class for creating new model
        filter_view_class(fields, view_name), # filter view class for filtering queryset
        table_view_class(fields, view_name), # table view class for displaying database table
        LogView,
    )

    # log view - adds 'log' to context - success/fail info set on as_view(log_status) call
    return type(view_name, view_classes, {})