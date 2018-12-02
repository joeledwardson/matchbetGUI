from django.views.generic import TemplateView
from django.shortcuts import reverse
from django.db.models.fields import DateTimeField
from django.utils.dateformat import format

from betlog.models import MyMoneyField
from betlog.names import viewname_app, model_update_viewname

datetime_format = lambda dt: format(dt, 'jS M y, H:i')

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


# get context data for table - saves to class instance (access as view.[variable] in template)
# to be used as a decorator
def get_table_context_data(get_context_data):

    def inner(self: TableView, **kwargs):

        context = get_context_data(self, **kwargs)

        # get query set
        qs = self.get_table_qs()

        # create db list of entries
        #   index 0 - object link
        #   index 1 - list of values
        #   index 2 - css formatting class
        table_list = [
            [
                self.get_object_link(o),
                [self.get_obj_attr(o, f) for f in self._field_names],
                self.get_css_rules(o)

            ] for o in qs]

        # assign to view
        self.table_list = table_list

        return context

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

