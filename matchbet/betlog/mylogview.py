from betlog.log import get_log_recent
from django.views.generic import TemplateView

# View with Log update
#   log_status is set upon calling as_view() so no need to set, only retrieve in get_context_data
class LogView(TemplateView):

    # 0 = no update, 1 = success, 2 = error
    log_status = 0

    # get log information and status
    def get_log_context_data(self):

        # set log - lines is log to display at bottom, status indicates highlight
        self.log= {'lines': get_log_recent(), 'status': self.log_status}

