from betlog.log import get_log_recent
from django.views.generic import TemplateView


# View with Log update
#   log_status is set upon calling as_view() so no need to set, only retrieve in get_context_data
class LogView(TemplateView):

    # 0 = no update, 1 = success, 2 = error
    log_status = 0


# get log information and status
# self.log_status should be set by as_view() from urls.py upon calling the view
# to be used as decorative function
def get_log_context_data(get_context_data):

    def inner(self: LogView, **kwargs):

        context = get_context_data(self, **kwargs)

        assert hasattr(self, 'log_status')

        # set log - lines is log to display at bottom, status indicates highlight
        context['log'] = {'lines': get_log_recent(), 'status': self.log_status}

        return context

    return inner