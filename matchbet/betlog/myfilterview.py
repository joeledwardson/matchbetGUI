from django.views.generic import TemplateView
from .filters import create_filter
from .models import fieldnames_all, fields_all
from .names import get_field_name

# CreatView class for filtering a queryset
#   MUST be derived with class that has a get_queryset() - e.g. ListView/CreateView
class FilterView(TemplateView):

    # abstract objects that must be initiated when class is created
    filter_class = None # class of filter to create

    # need to set filter instance on receiving get with filters in url
    def get(self, request, *args, **kwargs):

        # create filter instance
        self.filter = self.filter_class(request.GET, queryset=self.get_queryset())

        # return original get function - get_context_data will pull self.filter to template!
        return super().get(request, *args, **kwargs)


# create generic class based view
#   fields - django mode field list
#   field_names - names associated with [fields], for getting field values in table
#   field_friendly_names - friendly display names for table titles
def filter_view_class(fields, view_name):

    cls_name = 'View_filter_{}'.format(view_name)

    cls_dict = {
        'filter_class': create_filter(fields, view_name) # create filter class for model
    }

    # return new view class type
    return type(cls_name,(FilterView, ), cls_dict)