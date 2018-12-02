from django import template
from django.shortcuts import reverse

from betlog.views.views import view_classes
from betlog.names import viewname_app, model_viewname, model_name

import locale
locale.setlocale(locale.LC_ALL, '')

# create template library
register = template.Library()


# get model view name
@register.filter
def get_model_viewname(model):
    return model_viewname(model)

# get python view name including app name
@register.filter
def v(view_name):
    return viewname_app(view_name)

# get title from view
@register.filter
def title(view):
    return view.title if hasattr(view, 'title') else view.view_name

# get capitalised model class name
@register.filter
def get_model_name(model):
    return model_name(model)


# concatenate strings of vars
@register.simple_tag
def add_str(arg1, arg2):
    return str(arg1) + str(arg2)

# get view classes
@register.simple_tag
def get_view_classes():
    return [v['default'] for v in view_classes]

# get url from view name and view kwargs
@register.simple_tag
def get_url(view_name, kwargs):
    return reverse(viewname_app(view_name), kwargs=kwargs)

@register.simple_tag
def button_classes():
    return 'btn btn-info'

# retur value
@register.simple_tag
def r(value):
    return value