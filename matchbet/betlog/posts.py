#************************ Handle posts to server ***********************
from .log import server_logger
from .forms import form_classes
from .names import get_field_name

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

# create new object from post
def new_object(request, class_type):
    print(request.POST)
    form = create_form(class_type, request.POST)
    class_name = class_type._meta.verbose_name

    # check user data is valid in form
    if form.is_valid():
        o = class_type(**form.cleaned_data)
        o.save()
        server_logger.info('New {} "{}" added'.format(class_name, o))
        return True
    else:
        server_logger.error('New {} failed: {}'.format(class_name, errors_string(form)))
        return False
