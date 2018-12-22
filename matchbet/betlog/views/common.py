from betlog.views.create import create_view_class, CommonCreateView, CreateView
from betlog.views.message import set_message
from betlog.views.table import table_view_class, TableView, table_getter

from betlog.models import fields_all
from betlog.names import model_viewname, print_dict
from betlog.sessions import set_last_view
from betlog.filters import create_filter_set, Orderer, GenericFilterSet

from django.db.models import fields, DateTimeField, DateField, CharField
from typing import List

class CommonView(CommonCreateView, TableView):

    template_name = 'default.html'

    # model fitler class, set on creation of class
    filter_class = GenericFilterSet

    # model filter instance, set on get()
    filter_instance = None

    # Need to call individual context data assignments
    def get_context_data(self, **attrs):

        # need to set object to None of getobject from CreateView gets unhappy?
        # self.object = None

        # return create view context
        context = CreateView.get_context_data(self, **attrs)

        # add model to context
        context['model'] = self.model

        # add current url to context
        context['my_url'] = self.request.path

        return context

    # custom get queryset method for TableView - use filtered queryset
    def get_table_qs(self):
        return self.filter_instance.qs

    @table_getter
    @set_message
    @set_last_view
    def get(self, request, *args, **kwargs):

        # create filter instance from filter class
        self.filter_instance = self.filter_class(request.GET, queryset=self.get_queryset())

        # return CreateView().get
        response = CreateView.get(self, request, *args, **kwargs)

        return response

# get order_by
def get_default_ordering(fields: List[fields.Field]):

    # list of field types in order of priority, in which to order a queryset
    priorities = [
        DateTimeField,
        DateField,
        CharField
    ]

    # get list of fields (top priority first) of fields to order by
    top_choices = [f for p in priorities for f in fields if p==type(f)]

    # get first in list of top_choices, or if empty return first field
    field = next(iter(top_choices), fields[0])

    # if field is date or datetime, invert so get newest first
    if type(field) in [DateField, DateTimeField]:

        return Orderer.order_key(field.name, invert=True)

    else:
        # return field name
        return field.name


# create generic view - has a create view [form], filter embedded in [filter] and log. If date field exists than orders
# by newest first
def create_common_view(model) -> CommonView:

    print('Creating common view based on model "{}"'.format(model.__name__))

    # get view name from model
    view_name = model_viewname(model)

    # get fields from model
    fields = fields_all(model)

    # get default ordering from model fields
    ordering = get_default_ordering(fields)

    # create tuple of classes to include in common
    view_classes = (
        CommonView,
        create_view_class(model, view_name), # create view class for creating new model
        table_view_class(fields, view_name), # table view class for displaying database table
    )

    # create filter class based on model fields, with view name and default ordering
    filter_class = create_filter_set(fields, view_name, order_default=ordering)

    # log view - adds 'log' to context - success/fail info set on as_view(log_status) call
    return type(view_name, view_classes, {'filter_class': filter_class})