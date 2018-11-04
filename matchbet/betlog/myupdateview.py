from django.views.generic import UpdateView
from django.shortcuts import reverse, resolve_url
from django.urls import resolve

from .log import server_logger
from .names import viewname_info_app, viewname_app, model_viewname
from .forms import form_classes
from .sessions import get_last_view, get_last_view_kwargs


# Update view class - for editing an object instance
class CommonUpdateView(UpdateView):

    # abstract objects that must be initiated when class is created
    model = None
    form_class = None
    view_name = None # required for re-direct to post to with updated data

    # use update form - has different post action to standard form
    template_name = 'formupdate.html'

    # set view name to return to
    def set_from_viewname(self, request):

        # retrieve referer from request session - if does not exist use model default view
        self.from_viewname = get_last_view(request) or viewname_app(model_viewname(self.model))

        # retrieve referer view kwargs
        self.from_view_kwargs = get_last_view_kwargs(request) or {}

    # override post
    def post(self, request, *args, **kwargs):

        # set return view name - this is so get_success_url can read it
        self.set_from_viewname(request)

        return super().post(request, *args, **kwargs)

    # func called when a form is validated
    def form_valid(self, form):

        # get old object for log
        old_object = self.get_object()

        # call super to actally validate form
        redirect = super().form_valid(form)

        # update log
        server_logger.info('{} "{}" updated to "{}"'.format(self.model._meta.verbose_name,
                                                            old_object,
                                                            self.object))

        # return re-direction url - will either return to page or use success url
        return redirect

    # re-direct to original view_name
    def get_success_url(self):

        # append success to previous view name for re-direction
        return reverse(viewname_info_app(self.from_viewname, True), kwargs=self.from_view_kwargs)

    # override get function
    def get(self, request, *args, **kwargs):

        # set return view name - this so template can read it for cancel button
        self.set_from_viewname(request)

        # get current url - used as action of post in template
        self.my_url = request.path

        return super().get(request, *args, **kwargs)



# create generic class based view
def update_view_class(model, view_name):

    # create update view class name
    cls_update_name = 'View_Update_{}'.format(view_name)

    cls_dict = {
        'model': model, # this defines the model class
        'form_class': form_classes[model], # get form from form class dictionary
        'view_name': view_name, # assign view name
    }

    # create update view class
    return type(cls_update_name, (CommonUpdateView,), cls_dict)
