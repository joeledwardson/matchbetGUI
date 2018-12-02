from django.views.generic import TemplateView
from django.db.models import fields, DateTimeField, DateField, CharField
from django_filters import FilterSet
from typing import List

from betlog.filters import create_filter_set

# class for filtering a queryset
#   MUST be derived with class that has a get_queryset() - e.g. ListView/CreateView
class FilterView(TemplateView):

    # instance of filter_class created when get() called
    filter = None

    # abstract objects that must be initiated when class is created
    filter_class = None # class of filter to create

    def get_queryset(self):
        raise NotImplementedError


# set filter in self - to be used as a decorator function
def filter_get(get):

    # need to set filter instance on receiving get with filter_instances in url
    def inner(self: FilterView, request, *args, **kwargs):

        # create filter instance
        self.filter = self.filter_class(request.GET, queryset=self.get_queryset())

        # return original get function - get_context_data will pull self.filter to template!
        return get(self, request, *args, **kwargs)

    return inner


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

    # return field name
    return field.name


# create generic class based view
#   fields - django mode field list
#   field_names - names associated with [fields], for getting field values in table
#   field_friendly_names - friendly display names for table titles
def filter_view_class(fields, view_name) -> FilterView:

    cls_name = 'ViewFilter'.format(view_name)

    # get order_by and order_invert in dictionary
    ordering = get_default_ordering(fields)

    cls_dict = {
        'filter_class': create_filter_set(fields, view_name, order_default=ordering)
    }

    # return new view class type
    return type(cls_name,(FilterView, ), cls_dict)