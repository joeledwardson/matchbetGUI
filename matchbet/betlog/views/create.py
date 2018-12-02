from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.db.models import Model


from betlog.posts import new_object
from betlog.forms import form_classes

from .edit import GenericEditView, store_last_view, generic_edit_class

# CreatView common class - does NOT use view_kwargs!
class CommonCreateView(CreateView, GenericEditView):

    # received request for new object instance
    @store_last_view # store last view name & kwargs in self
    def post(self, request, *args, **kwargs):

        # create new object (auto saves it)
        success = new_object(request, self.model)

        # redirect to same page - add succes of creation to url to update user
        return HttpResponseRedirect(self.get_return_info_url(success))


# create generic class based view
def create_view_class(model, view_name) -> CommonCreateView:

    # use edit class generator to set model, view name and form, with 'Create' as class name and using CommonCreateView
    return generic_edit_class(
        model=model,
        cls=CommonCreateView,
        edit_type='Create',
        view_name=view_name
    )