from .apps import BetlogConfig
from django.db.models import fields

css_checkbox_class = 'class-checkbox'
css_select_class = 'class-selector'
css_date_class = 'class-date-picker'
css_time_class = 'class-time-picker'
date_format = 'dd-mm-yyyy'

numeric_fields = [fields.IntegerField, fields.DecimalField, fields.FloatField]


# ONLY applicable to this scope!
# create a view name from a django model
def model_viewname(model):
    return model._meta.verbose_name_plural.capitalize().strip()

# create an update view name from a django model
def model_update_viewname(model):
    return '{}_update'.format(model_viewname(model))

def get_field_name(cls, arg):
    return cls._meta.get_field(arg).verbose_name


# for a POST, append view name with either "success" or "failure"
def _append_success(v, success):
    return '{}_{}'.format(v, 'success' if success else 'failure')

# add app name to view name (required for calling reverse)
def viewname_app(v):
    return '{}:{}'.format(BetlogConfig.name, v)

# add app name to view name (required for calling reverse), append with "success" or "failure", denoting info
def viewname_info_app(v, success):
    return _append_success(viewname_app(v), success)

