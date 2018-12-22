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

    def get_forms(self, site):

        # forms initial data is the site pk (site is hidden to user)
        initial={siteFieldName: site.pk}

        # create blank array to assign forms
        forms = {}

        # assign form instances using form classes
        for model in models:
            forms[model] = self.form_classes[model](initial=initial)

        # return array of forms
        return forms