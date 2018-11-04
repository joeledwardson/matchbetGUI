from django.views.generic import TemplateView
from .names import viewname_app, model_update_viewname
from django.shortcuts import reverse
from .models import MyMoneyField


# view for database table
#   MUST be derived with a class which has
#       get_table_qs() - for retrieving queryset for table
#       view_name - required for forming return-to view for update link
#   If css_rules are specified, list of:
#       rule - function to check object against
#       css_class - css class to set validation pass
class TableView(TemplateView):

    # retrieve queryset to display in table - MUST be derived
    def get_table_qs(self):
        pass

    def object_update_link(self, object):
        return reverse(
            viewname_app(model_update_viewname(type(object))),
            kwargs={'pk': object.pk}
        )

    # get link target for object in table - by default is update link
    def get_object_link(self, object):
        return self.object_update_link(object)

    # get context data for table - saves to class instance (access as view.[variable] in template)
    def get_table_context_data(self):

        # get query set
        qs = self.get_table_qs()

        # format money fields with £ if they of money type
        def getobjattr(o, field_name):
            v = getattr(o, field_name)
            return MyMoneyField.money_str(v) if field_name in self._money_fields else v

        def get_css_rules(o):
            for r in self.css_rules:
                if r['rule'](o):
                    return r['css_class']
            return None

        # create db list of entries
        #   index 0 - object link
        #   index 1 - list of values
        #   index 2 - css formatting class
        table_list = [
            [
                self.get_object_link(o),
                [str(getobjattr(o, f)) for f in self._field_names],
                get_css_rules(o) if hasattr(self, 'css_rules') else None

            ] for o in qs]

        # assign to view
        self.table_list = table_list

# create table class based on field list and view name
def table_view_class(fields, view_name):

    class_name = 'View_Table_'.format(view_name)

    # class dictionary for class
    cls_dict = {
        '_money_fields': [f.name for f in fields if type(f) == MyMoneyField], # add list of fields names for money fields
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

