from django.views.generic import TemplateView
from django.shortcuts import reverse, render
from django.db.models.fields import DateTimeField
from django.utils.dateformat import format
from django.http import JsonResponse

from betlog.models import MyMoneyField
from betlog.names import viewname_app, model_update_viewname

# step size - number of database elements to load at a time
TABLE_STEP_SIZE = 10

# get list slice using step size
def list_slice(l, step, i):
    return l[slice(step*i, step*(i+1))]


# date time format is day of month (j), suffix (S), 3 letter month (M), 2 letter year (y) , 24-hour (H), minutes (i)
# e.g. 31st Jan, 19:21
datetime_format = lambda dt: format(dt, 'jS M y, H:i')

# default field formatters to apply to table elements  when creating from queryset
field_formatters = {
    MyMoneyField: MyMoneyField.money_str,
    DateTimeField: datetime_format,
}

# view for database table
#   MUST be derived with a class which has
#       get_table_qs() - for retrieving queryset for table
#       view_name - required for forming return-to view for update link
class TableView(TemplateView):

    _table_formatters = None
    _field_names = None
    field_titles = None
    css_rules = {}

    # Set css rules: , list of:
    #       rule - function to check object against
    #       css_class - css class to set validation pass
    @classmethod
    def set_css_rules(cls, css_rules):
        cls.css_rules = css_rules

    # get css rule (currently ONLY 1 supported per item) - check rules against object o
    @classmethod
    def get_css_rules(cls, o):
        for r in cls.css_rules:
            if r['rule'](o):
                return r['css_class']
        return None

    # retrieve queryset to display in table - MUST be derived
    def get_table_qs(self):
        raise NotImplementedError

    def object_update_link(self, object):

        return reverse(
            viewname_app(model_update_viewname(type(object))),
            kwargs={'pk': object.pk}
        )

    # get link target for object in table - by default is update link
    def get_object_link(self, object):

        return self.object_update_link(object)


    # format money fields with £ if they of money type
    def get_obj_attr(self, o, field_name):

        v = getattr(o, field_name)

        return self._table_formatters[field_name](v)

    # get db table data from queryset, formatted into template form
    #   index 0 - object link
    #   index 1 - list of values
    #   index 2 - css formatting class
    def get_template_table(self, qs):

        return [
            [
                self.get_object_link(o),
                [self.get_obj_attr(o, f) for f in self._field_names],
                self.get_css_rules(o)

            ] for o in qs]


# table get wrapper - if pg_num is specified return a dict containing
#   table_list: next values in table
#   end: boolean value, if true means are at end of table
def table_getter(get):

    # inner function to wrap around get
    def inner(self: TableView, request, *args, **kwargs):

        # get page number pg_num from kwargs
        pg = kwargs.get('pg_num')

        if pg is not None:

            # request is ajax for more content, use page number for slice
            qs =  list_slice(self.get_table_qs(), TABLE_STEP_SIZE, pg)

            # get template formatted table rows
            rows = self.get_template_table(qs)

            data = {
                # set boolean value to true if reached end of table
                'end': qs is not None,

                # render the "table_rows" file using the slice, takes [table_rows] as an input
                'table_data': render(request, "table_rows.html", {'table_rows': rows})
            }

            # return Json data
            return JsonResponse(data)

        else:
            # no pg_num var, render page as normal

            # call get() first, probably required to set qs before retrieval
            response = get(self, request, *args, **kwargs)

            # get first slice query set
            qs =  list_slice(self.get_table_qs(), TABLE_STEP_SIZE, 0)

            # get template formatted table list and assign to view
            self.table_list = self.get_template_table(qs)

            # return original response
            return response

    return inner

# create table class based on field list and view name
def table_view_class(fields, view_name, field_formatters=field_formatters) -> TableView:

    class_name = 'ViewTable'.format(view_name)

    # function that returns same value
    val = lambda v:v

    # table formatters - apply custom formatting to specefic type of fields - if not in list return same value
    table_formatters = {
        field.name: field_formatters.get(type(field)) or val for field in fields
    }

    # class dictionary for class
    cls_dict = {
        '_table_formatters': table_formatters,
        '_field_names': [f.name for f in fields], # use underscore as this should only be accessed in class method, not in template
        'field_titles': [f.verbose_name for f in fields], # field titles for template to print
    }

    return type(class_name, (TableView, ), cls_dict)

# returns dictionary mapping
#   rule - function which checks field value from an object - takes [object] and [field_type] as arguments
#   goodVal - value that [field_type] passed to rule should be equal to, for assignment of css field
#   field_val_getter - function to retrive fields' value. By default it retrives .name for the ModelType custom model
def css_good_type(field_type, goodVal, field_val_getter = lambda f: getattr(f, 'name')):
    return {
        'rule': lambda object: field_val_getter(getattr(object, field_type)) == goodVal,
        'css_class': 'row-green' #   css_class - 'good', green highlight css class to apply in template if rule() returns true
    }


# returns dictionary mapping
#   rule - function which checks field value from an object - takes [object] and [field_type] as arguments
#   goodVal - value that [field_type] passed to rule should be equal to, for assignment of css field
#   field_val_getter - function to retrive fields' value. By default it retrives .name for the ModelType custom model
def css_bad_type(field_type, badVal, field_val_getter = lambda f: getattr(f, 'name')):
    return {
        'rule': lambda object: field_val_getter(getattr(object, field_type)) == badVal,
        'css_class': 'row-red'
    }

