from django import template
from django.shortcuts import reverse

from betlog.views import view_classes
from betlog.names import viewname_app

# create template library
register = template.Library()


# get title from view
@register.filter
def title(view):
    return view.title if hasattr(view, 'title') else view.view_name

# get capitalised model class name
@register.filter
def title_name(cls):
    return cls._meta.verbose_name.capitalize()

# get view classes
@register.simple_tag
def get_view_classes():
    return [v['default'] for v in view_classes]

# get python view name including app name
@register.filter
def v(view_name):
    return viewname_app(view_name)

@register.simple_tag
def get_url(view_name, kwargs):
    return reverse(viewname_app(view_name), kwargs=kwargs)

@register.simple_tag
def button_classes():
    return 'ui-button ui-widget ui-corner-all'