# wrapper for get function which sets the current view in session
#   view [self] MUST contain view_name
#   view [self] can optionally contain view_kwargs
def set_last_view(get):

    # inner function to wrap around get
    def set_last_view(self, request, *args, **kwargs):

        # first, get response (get function may need to set [view_kwargs])
        response = get(self, request, *args, **kwargs)

        # set last view to current view name
        request.session['last_view'] = self.view_name

        if hasattr(self, 'view_kwargs'):
            # if exists, set view kwargs to current view kwargs
            request.session['last_view_kwargs'] = self.view_kwargs

        else:
            # view key word args does not exist, clear!
            request.session['last_view_kwargs'] = {}

        # return original response from get function
        return response

    # return inner function
    return set_last_view


# retrieve last view name
def get_last_view(request):
    return request.session.get('last_view')

# retrieve last view kwargs (may return none)
def get_last_view_kwargs(request):
    return request.session.get('last_view_kwargs')