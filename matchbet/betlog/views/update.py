from django.views.generic import UpdateView
from django.db.models import Model
from django.http import HttpResponseRedirect

from betlog.log import server_logger
from betlog.names import model_name, model_update_viewname, model_delete_viewname, viewname_app

from .edit import GenericEditView, store_last_view, generic_edit_class


# func to call to delete object
def delete(object):

    # get object string
    object_str = str(object)

    # delete object
    object.delete()

    # update logger
    server_logger.info('Successfully deleted {model}: {object}'.format(
        model=model_name(object._meta.model),
        object=object_str,
    ))


# Update view class - for editing an object instance
class CommonUpdateView(GenericEditView, UpdateView):

    view_name = None # required for re-direct to post to with updated data
    delete_url = None # url for deleting object
    allow_delete = True # if false, don't allow deleting of objects

    # use update form - has different post action to standard form
    template_name = 'formupdate.html'

    # override post() - store last view in self.from_view_name and self.from_view_kwargs so get_success_url can read it
    post = store_last_view(UpdateView.post)

    # override context data getter
    def get_context_data(self, **kwargs):

        # get context from django Update view
        context = UpdateView.get_context_data(self, **kwargs)

        # set form post url
        context['form_url'] = self.get_return_url()

        # set form title
        context['form_title'] = 'Update {}'.format(model_name(self.model))

        return context

    # func called when a form is validated
    def form_valid(self, form):

        # get old object for log
        old_object = self.get_object()

        # call super to actually validate form
        redirect = super().form_valid(form)

        # update log
        server_logger.info('{model} {old} updated to {new}'.format(
            model=model_name(self.model),
            old=old_object,
            new=self.object)
        )

        # return re-direction url - will either return to page or use success url
        return redirect

    # override get function - store last view name & kwrags this so template can read it for cancel button
    @store_last_view
    def get(self, request, *args, **kwargs):

        # get current url - used as action of post in template
        # self.my_url = request.path

        # get previous url to return to on cancel
        # self.cancel_url = self.get_return_url()

        return super().get(request, *args, **kwargs)

    # override post function to handle deletions
    @store_last_view
    def post(self, request, *args, **kwargs):

        # check if delete button was pressed
        if 'delete_button' in request.POST:

            # check if model is allowed to be deleted
            if self.allow_delete:

                # delete object
                delete(self.get_object())

                # go to previous view with success
                return HttpResponseRedirect(self.get_success_url())

            else:

                # delete requested but not allowed
                server_logger.error('You cannot delete a {}'.format(model_name(self.model)))

                # go to previous view with fail
                return HttpResponseRedirect(self.get_return_info_url(success=False))

        else:

            # update object
            return super().post(request, *args, **kwargs)


    # func called on successful post - return previous view with success appended to url
    def get_success_url(self):
        return self.get_return_info_url(success=True)



# create generic class based view
def update_view_class(model: Model) -> CommonUpdateView:

    # generate view name from model
    view_name = model_update_viewname(model)

    # use edit class generator to set model, view name and form, with 'Update' as class name and using CommonUpdateView
    return generic_edit_class(
        model=model,
        cls=CommonUpdateView,
        edit_type='Update',
        view_name=view_name
    )
