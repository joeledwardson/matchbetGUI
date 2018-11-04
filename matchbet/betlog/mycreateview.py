from django.views.generic import CreateView
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from .posts import new_object
from .names import viewname_info_app
from .forms import form_classes

# CreatView common class
class CommonCreateView(CreateView):

    # abstract objects that must be initiated when class is created
    model = None
    form_class = None
    view_name = None # required for link in template to

    # received request for new object instance
    def post(self, request, *args, **kwargs):

        # create new object (auto saves it)
        success = new_object(request, self.model)

        # get variable name for current view - add succes of creation to url to update user
        post_name = viewname_info_app(self.view_name, success)

        # redirect to same page
        return HttpResponseRedirect(reverse(post_name))


#TODO make generic for udpate and create
# create generic class based view
def create_view_class(model, view_name):

    cls_name = 'View_Create_{}'.format(view_name)

    cls_dict = {
        'model': model, # this defines the model
        'form_class': form_classes[model], # get form from form class dictionary
        'view_name': view_name, # assign view name
    }

    # return new view class type
    return type(cls_name,(CommonCreateView, ), cls_dict)