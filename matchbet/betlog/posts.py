#************************ Handle posts to server ***********************
from .log import server_logger
from .forms import form_classes
from .names import get_field_name, model_name

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

        # update log file new model
        server_logger.info('New {model} added: {object}'.format(model=class_name, object=obj))

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
