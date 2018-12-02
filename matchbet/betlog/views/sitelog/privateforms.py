from django import forms as django_forms
from django.views.generic.base import TemplateView
from django.forms.models import ModelForm

from betlog.forms import create_form_type
from .globals import siteFieldName, models


# create form class based on model - using hidden input for site field
def create_form_class(model) -> ModelForm:

    # pass hidden input as widget for site field in custom fields argument
    return create_form_type(
        model_type=model,
        custom_fields={
            siteFieldName: django_forms.CharField(
                widget=django_forms.HiddenInput()
            )
    })

# Form view
#   Form_Transaction_Class and Form_Bet_Class form the classes to instantiate forms
class SiteLog_FormView(TemplateView):

    form_classes = {model: create_form_class(model) for model in models}
    forms = {model: None for model in models}

    site = None

# decorative function to be called over get
#   get() MUST define self.site
#   func sets self.form_bet and self.form_transaction instances
def update_forms(get):

    def inner(self: SiteLog_FormView, request, *args, **kwargs):

        initial={siteFieldName: self.site.pk}

        # assign form instances using form classes
        for mdl in self.form_classes:
            self.forms[mdl] = self.form_classes[mdl](initial=initial)

        return get(self, request, *args, **kwargs)

    return inner