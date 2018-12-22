from django.db.models import fields

from .apps import BetlogConfig
from .models import MyMoneyField

numeric_fields = (
    fields.IntegerField,
    fields.DecimalField,
    fields.FloatField,
    MyMoneyField
)

date_fields = (
    fields.DateTimeField,
    fields.DateField
)

# view name of a django model - get stripped, capitalised, verbose (plural) name
def model_viewname(model):
    return model._meta.verbose_name_plural.capitalize().strip()

# name of a django model - get stripped capitalised verbose (singular) name
def model_name(model):
    return model._meta.verbose_name.capitalize().strip()

# create an update view name from a django model
def model_update_viewname(model):
    return '{}_update'.format(model_viewname(model))

def get_field_name(cls, arg):
    return cls._meta.get_field(arg).verbose_name

# add app name to view name (required for calling reverse)
def viewname_app(v):
    return '{}:{}'.format(BetlogConfig.name, v)

# print a dictionary
def print_dict(d: dict, nm: str):

    print('Printing contents of dictionary: {}'.format(nm))

    for key in d:
        print('{}: {}'.format(key, d[key]))