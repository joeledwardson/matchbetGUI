def set_last_view(request, view_name, kwargs={}):
    request.session['last_view'] = view_name
    request.session['last_view_kwargs'] = kwargs

def get_last_view(request):
    return request.session.get('last_view')

def get_last_view_kwargs(request):
    return request.session.get('last_view_kwargs')