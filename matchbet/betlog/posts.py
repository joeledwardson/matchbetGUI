#************************ Handle posts to server ***********************
from .log import server_logger
from .forms import form_classes
from .names import get_field_name, model_name
from .models import SiteExchange

is_site_exchange = lambda model_object: issubclass(type(model_object), SiteExchange)

# get form errors in string form
# typical format
# form.errors = {
#     'username':
#         ['This name is reserved and cannot be registered.'],
#     'password2':
#         ['This password is too short. It must contain at least 8 characters.',
#          'This password is too common.']
# }
def errors_string(form):
    # get class type
    cls = form.Meta.model

    # get errors in dictionary form
    errors = form.errors.as_data()

    # get dictionary keys
    keys = errors.keys()

    # loop keys - [k] e.g. username, password 2
    #   loop list of errors [e] for key [k]
    #       get verbose name from class [cls] with key [k] and join list [e] together
    error_list = ['{} - {}'.format(get_field_name(cls, k), ''.join(e)) for k in keys for e in errors[k]]
    return ' '.join(error_list)


# create form instance from class type and post data
def create_form(cls, post):

    # create form class
    Form = form_classes[cls]

    # create form form posted data
    return Form(post)


# create new object from post - return True on success, False on fail
def new_object(request, class_type):

    # get form instance from post
    form = create_form(class_type, request.POST)

    # get model name
    class_name = model_name(class_type)

    # check user data is valid in form
    if form.is_valid():

        # create object from form data
        obj = class_type(**form.cleaned_data)

        # save object in database
        obj.save()

        # add balance adjust to site balance (if is exchange type)
        if is_site_exchange(obj):
            obj.site.update_balance(obj.balanceAdjust)

        # update log file new model
        server_logger.info('New {model}: {object}'.format(model=class_name, object=obj))

        # success
        return True

    else:

        # update log file with errors
        server_logger.error('New {model} failed: {errors}'.format(
            model=class_name,
            errors=errors_string(form)
        ))

        # failure
        return False


# func to call to delete object
def delete(obj):

    # get object string
    object_str = str(obj)

    # reverse site balance adjustment (if is exchange type)
    if is_site_exchange(obj):
        obj.site.update_balance(-1 * obj.balanceAdjust)

    # delete object
    obj.delete()

    # update logger
    server_logger.info('Deleted {model}: {object}'.format(
        model=model_name(obj._meta.model),
        object=object_str,
    ))


# func to call on updating an object
def update(new_object):

    # update log
    server_logger.info('Updated: {}'.format(new_object))

    # re-calculate site balance (if is exchange type)
    if is_site_exchange(new_object):
        new_object.site.calculate_balance()