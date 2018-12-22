from betlog.log import get_log
from django.views.generic import TemplateView

# set message in self (Template View) - to be used as a decorator function
def set_message(get):

    # need to set filter instance on receiving get with filter_instances in url
    def inner(self: TemplateView, request, *args, **kwargs):

        # get message indicator variable
        message_var = kwargs.get('message_var')

        # if variable passed then set string to empty so use not prompted on loading page
        if not message_var:

            msg = ""

        else:
            # get first line from Log
            msg = next(iter(get_log()))

            # take only first 26 chars (to account for date and time), strip new line so doesn't break javascript
            msg = msg[26:].strip('\n')

        self.message = msg

        # return original get function - get_context_data will pull self.filter to template!
        return get(self, request, *args, **kwargs)

    return inner