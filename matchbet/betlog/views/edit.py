from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import reverse
from django.db.models import Model

from betlog.sessions import get_last_view_name, get_last_view_kwargs
from betlog.names import viewname_app, model_viewname, model_name
from betlog.forms import form_classes

class GenericEditView(SingleObjectMixin):

    from_view_name = None # view name  to return to - should be stored in session
    from_view_kwargs = None # returning view name kwargs - can be stored in session (optional)

    # re-direct to last view with success in url
    def get_return_info_url(self, success=True):

        # initialise kwargs dict with from view kwargs or set to empty dict
        kwargs = self.from_view_kwargs or {}

        # set message variable to prompt alert on loading webpage
        kwargs['message_var'] = success

        # append success to previous view name for re-direction
        return reverse(
            viewname_app(self.from_view_name),
            kwargs=kwargs
        )

    # re-direct to last view (no info)
    def get_return_url(self):

        # initialise kwargs dict with from view kwargs or set to empty dict
        kwargs = self.from_view_kwargs or {}

        # delete message variable so on returning with no update, not prompted with message
        kwargs.pop('message_var', None)

        # get previous view name and kwargs
        return reverse(
            viewname_app(self.from_view_name),
            kwargs=kwargs
        )

# func to store from_view_name and from_view_kwargs from session into self
# use to decorate get() or post()
def store_last_view(get_post):

    # set view name to return to
    def inner(self: GenericEditView, request, *args, **kwargs):

        # retrieve referer from request session
        self.from_view_name = get_last_view_name(request)

        # check exists
        if self.from_view_name:

            # retrieve referer view kwargs (if exist)
            self.from_view_kwargs = get_last_view_kwargs(request) or {}

        else:

            # last view doesn't exist - use model
            viewname_app(model_viewname(self.model))

            # model views have no kwargs
            self.from_view_kwargs = {}

        # call original get function
        return get_post(self, request, *args, **kwargs)

    return inner


def generic_edit_class(model: Model, cls, edit_type: str, view_name: str):

    cls_name = 'View{type}{model}'.format(
        type=edit_type,
        model=model_name(model)
    )

    cls_dict = {
        'model': model,  # this defines the model
        'form_class': form_classes[model],  # get form from form class dictionary
        'view_name': view_name,  # assign view name
    }

    # return new view class type
    return type(cls_name, (cls, GenericEditView), cls_dict)