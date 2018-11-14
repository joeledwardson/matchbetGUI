
# get_dict = request.GET.copy()
# # filter to site by the [site] object stored in class
# site_filter = {siteFieldName: site}
#
#
# qs_t = Transaction.objects.filter(**site_filter)
# qs_b = Bet.objects.filter(**site_filter)
#
# # copy transaction type to bet type for filtering
# t = get_dict.get(objectType.name)
# if t:
#     filter_dict = {type_name(transactionTypeField): t}
#     qs_t = qs_t.filter(**filter_dict)
#
#     filter_dict = {type_name(betTypeField): t}
#     qs_b = qs_b.filter(**filter_dict)
#
#     get_dict.pop(transactionTypeField)
#
# def get_filter(qs):
#     return self.filter_class(get_dict,
#                              queryset=qs)
#
# filter_transaction = get_filter(qs_t)
# filter_bet = get_filter(qs_b)
#
# def annotate(qs, type_field):
#     # qs = model._default_manager.filter(**site_filter)
#     annotation = {objectType.name: F('{}__name'.format(type_field))}
#     return qs.annotate(**annotation)
#
# # qs_t = filter_transaction.qs
# qs_t = annotate(filter_transaction.qs, transactionTypeField)
# qs_b = annotate(filter_bet.qs, betTypeField)
#
# order_by = get_dict.get('o') or 'date'
# # if order_by:
# #     order_reversed = not(order_by.startswith('-'))
# #     order_by.strip('-')
# # else:
# #     order_reversed = True
# #     order_by = 'date'
#
# # join queryset together and order by date (inverted so newest first)
# self.qs = sorted(
#     chain(qs_t, qs_b),
#     key=attrgetter(order_by),
#     reverse=True
# )
# # filter to site by its name
# site_filter = {siteFieldName: self.site}
#
# # transaction annotation query
# query_t = {objectType.name: F('{}__name'.format(transactionTypeField))}
#
# # filter transactions by site name
# filtered_t = Transaction._default_manager.filter(**site_filter)
# #
# # # transaction annotated queryset
# # qs_t = filtered_t.annotate(**query_t)
# #
# # qs_t = self.filter_class(get,
# #                          queryset=Transaction._default_manager.filter(**site_filter))
#
# # bet annotation query
# query_b = {objectType.name: F('{}__name'.format(betTypeField))}
#
# # filter bets by site name
# filtered_b = Bet._default_manager.filter(**site_filter)
#
# print(filtered_b)
#
# # bet annotated queryset
# qs_b = filtered_b.annotate(**query_b)
#
#
# # join queryset together and order by date (inverted so newest first)
# return sorted(
#     chain(qs_t, qs_b),
#     key=attrgetter('date'),
#     reverse=True
# )
# # determine if instance is of django money type
# @register.filter
# def is_money_field(field_string):
#     return type(field_string) == MyMoneyField
#
# @register.filter
# def money_str(amount):
#     return MyMoneyField.money_str(amount)
# get plural capitalised model class name
# @register.filter
# def title_name_plural(cls):
#     return cls._meta.verbose_name_plural.capitalize()

# get view name for updating an object (including app name)
# @register.filter
# def u_ob(object):
#     return viewname_app(model_update_viewname(type(object)))


# get attribute from model instance
# @register.filter
# def get_field(cls, attr):
#     val = getattr(cls, attr)
#     return val
# # get model field verbose_name - (use for printing)
# @register.filter
# def get_name(cls, arg):
#     return get_field_name(cls, arg)
#
# # get return viewname (variable name not actual return view name)
# @register.simple_tag
# def get_var_return_viewname():
#     return var_from_viewname
#
# class Meta:
#     pass
# print('broken:')
# for f in fields_dict:
#     print('{}: {}'.format(f, fields_dict[f]))


# Meta.fields = [field.name for field in fields if field.name in fields_dict]
#
# fields_dict2 = {field.name:
# form_filter['filter'](
#     widget=form_filter['widget'](
#         attrs={**(form_filter.get('widget_attrs') or {}), 'id':'id_{}_{}'.format(cls_name, field.name)}
#     ) if form_filter.get('widget') else None,
#     field_name=field.name,
#     # **({'queryset':type(field.related_model())._default_manager.all()} if type(field) == models.ForeignKey else {})
# )
# for field in model_fields for form_filter in form_filters if type(field) in form_filter['fields'] }
# # print('working:')
# for f in fields_dict2:
#     print('{}: {}'.format(f, fields_dict2[f]))


# only include fields which have been used for filter or foreign keys (which automatically create dropdown)
# Meta.fields = [field.name for field in model_fields if field.name in fields_dict or type(field) == models.ForeignKey]

# // toggle an object to display or hide - update button text on action
# function ToggleObject(button, objectId, prompts, displays={true: 'block', false: 'none'}) {
#
#     // get form object
#     object = document.getElementById(objectId);
#
#     // determine if object is active - use false lookup in case display is different from block?
#     objectActive = !(object.style.display == displays[false]);
#
#     // toggle display
#     object.style.display = displays[!objectActive];
#
#     // change button value
#     button.value = prompts[!objectActive];
#
# }


# # TODO add default log_status as 0 in urls
# # If as_view() called without log_status then default to 0 so no highlighting
# @classmethod
# def as_view(cls, **initkwargs):
#
#     # check for log status argument in key word arguments
#     if 'log_status' not in initkwargs:
#
#         # not found - reset to 0 so self.log.status will be set to 0
#         initkwargs['log_status'] = 0
#
#     # return super of same function
#     return super().as_view(**initkwargs)
# import django_filters
# from django_filters import widgets as filter_widgets
#
# from django.db import models
# from django.shortcuts import get_object_or_404, reverse, render
# from django.http import HttpResponseRedirect
# from django.views.generic import ListView, UpdateView, CreateView
# from django.utils.translation import ugettext_lazy as _
# from django.forms import widgets
# from django import forms
#
# from betlog.models import Site, Transaction, Bet, Match, fieldnames_all, fields_all
# from betlog.log import get_log_recent
# from betlog.posts import new_object, errors_string
# from betlog.names import construct_viewname, construct_viewname_info, css_date_class
# from betlog.forms import  form_classes
# from betlog.log import server_logger
#
#
#
#
# date_range_widget = lambda: filter_widgets.RangeWidget(attrs={'class': css_date_class, 'placeholder':'dd/mm/yyyy'})
#
# # CreatView common class
# class CommonView(CreateView):
#     # MUST derive custom model not leave this
#     model = models.Model
#
#     # use test html during dev - TODO
#     template_name = 'test.html'
#
#     # 0 = no update, 1 = success, 2 = error
#     log_status = 0
#
#     # wrapper for get_context_data in case added functionality is required
#     def _get_context_data(self, **kwargs):
#
#         # get [form] from CreateView
#         context = super(CreateView, self).get_context_data(**kwargs)
#
#         # set log - lines is log to display at bottom, status indicates highlight
#         context['log'] = {'lines': get_log_recent(), 'status': self.log_status}
#
#         # Add object list - can derive get_queryset in children
#         # context['object_list'] = self.get_queryset()
#
#         # add filter data instance
#         context['filter'] = self.filter
#
#         # return updated context
#         return context
#
#     # assign wrapper function - this is default unless specified otherwise in child
#     get_context_data = _get_context_data
#
#
#     # received request for new object instance
#     def post(self, request, *args, **kwargs):
#
#         # create new object (auto saves it)
#         success = new_object(request, self.model)
#
#         # get variable name for current view - add succes of creation to url to update user
#         post_name = construct_viewname_info(self.view_name, success)
#
#         # redirect to same page
#         return HttpResponseRedirect(reverse(post_name))
#
#     def get(self, request, *args, **kwargs):
#
#         # create filter instance
#         self.filter = self.filter_class(request.GET, queryset=self.model.objects.all())
#
#         # return original get function - get_context_data will pull self.filter to template!
#         return super().get(request, *args, **kwargs)
#
#
#     # If as_view() called without log_status then default to 0 so no highlighting
#     @classmethod
#     def as_view(cls, **initkwargs):
#
#         # check for log status argument in key word arguments
#         if 'log_status' not in initkwargs:
#
#             # not found - reset to 0 so self.log.status will be set to 0
#             initkwargs['log_status'] = 0
#
#         # return super of same function
#         return super().as_view(**initkwargs)
#
#
#
#
#
#
# # Update view class - for editing an object instance
# class CommonUpdateView(UpdateView):
#
#     # use update form - has different post action to standard form
#     template_name = 'formupdate.html'
#
#     # func called when a form is validated
#     def form_valid(self, form):
#
#         # get old object for log
#         old_object = self.get_object()
#
#         # call super to actally validate form
#         r = super().form_valid(form)
#
#         # update log
#         server_logger.info('{} "{}" updated to "{}"'.format(self.model._meta.verbose_name,
#                                                             old_object,
#                                                             self.object))
#         return r
#
#     # re-direct to original view_name (without update) with log update success
#     def get_success_url(self):
#         return reverse(construct_viewname_info(self.view_name, True))
#
#
# # by default no select boolean widget displays 'Uknown' - use blank text for no selection
# class FriendlyBooleanWidget(filter_widgets.BooleanWidget):
#     def __init__(self, attrs):
#         choices = (('', _('')),
#                    ('true', _('Yes')),
#                    ('false', _('No')))
#
#         # skip BooleanWidget init and go straight to Choice widget super - override choices
#         return super(forms.Select, self).__init__(attrs=attrs, choices=choices)
#
# form_filters = [
#     {
#         'fields': [models.DateField, models.DateTimeField],
#         'filter': django_filters.DateFromToRangeFilter,
#         'widget': filter_widgets.RangeWidget,
#         'attrs': {'class': css_date_class, 'placeholder': 'dd/mm/yyyy'}
#     },
#     {
#         'fields': [models.BooleanField],
#         'filter': django_filters.BooleanFilter,
#         'widget': FriendlyBooleanWidget,
#         'attrs': {}
#     },
#
# ]
#
#
#
# # create filter class based on model
# def create_fitler(model_class):
#     # first set name
#     cls_name = '_Filter{}'.format(model_class.__name__)
#
#     # list of fields in the model
#     model_fields = fields_all(model_class)
#
#     # create dictionary of Meta class variables
#     class Meta:
#         model = model_class
#         fields = fieldnames_all(model_class) # list of field names in the model
#
#     # map dict of field names with their filters and assigned widgets
#     fields_dict = {field.name:
#         form_filter['filter'](
#             widget=form_filter['widget'](
#                 attrs=form_filter['attrs']
#             ),
#             field_name=field.name)
#         for field in model_fields for form_filter in form_filters if type(field) in form_filter['fields'] }
#
#     # create class type
#     return type(cls_name, (django_filters.FilterSet,), {'Meta': Meta, **fields_dict})
#
#
#
#
# # create generic class based view
# def create_view(cls):
#
#     # use class name for django view name
#     name = cls.__name__
#     cls_name = '_View{}'.format(name)
#
#     # create update view class name
#     cls_update_name = '_ViewUpdate{}'.format(name)
#
#     cls_dict = {
#         'model': cls, # this defines the model - required for UpdateView
#         'form_class': form_classes[cls], # get form from form class dictionary
#         'view_name': name, # assign view name
#         'filter_class': create_fitler(cls) # create filter class for model
#     }
#
#     # create update view class
#     ClsUpdateView = type(cls_update_name, (CommonUpdateView,), cls_dict)
#
#     # add model fields to class - used in template to render table
#     cls_dict['object_fields'] = fieldnames_all(cls)
#
#     # add view update class type
#     cls_dict['Update'] = ClsUpdateView
#
#     # return new view class type
#     return type(cls_name,(CommonView,), cls_dict)
#
# # create site view - custom queryset function to order by name
# def get_site_queryset(self):
#     return self.model.objects.order_by('name')
# SiteView = create_view(Site)
# SiteView.get_queryset = get_site_queryset
#
# TransactionView = create_view(Transaction)
#
# # TransactionView.filter = create_fitler(Transaction)({}, Transaction.objects.all())
#
# # create match view class
# MatchView = create_view(Match)
#
# # create bet view class
# BetView = create_view(Bet)
#
# # default view is site view
# DefaultView = SiteView
#
# # array of view classes- to be accessed in urls
# views_classes = [SiteView, MatchView, BetView, TransactionView]
#


# def form_field_widgets(fields):
#
#     fields_dict = {}
#
#     date_widget = lambda i: django_filters.widgets.RangeWidget(
#         attrs={
#             'class': css_date_class,
#             'placeholder': 'dd/mm/yyyy',
#             'id': 'filter_date_{}'.format(i)
#         })
#
#     date_filter = lambda i: django_filters.DateFromToRangeFilter(
#         widget=date_widget(i))
#
#     # fields to apply date range widget to
#     dateRangeFields = [models.DateField, models.DateTimeField]
#
#     date_dict = {field.name: django_filters.DateFromToRangeFilter(
#         widget=date_widget(i),
#         field_name=field.name)
#         for i, field in enumerate(fields) if type(field) in dateRangeFields}
#
#     bool_didct =
#         {field.name: django_filters.BooleanFilter(widget=FriendlyBooleanWidget())})
#         for field in model_fields if type(field) == models.BooleanField
#     ]

# create dictionary of date fields - adding widget with custom css class, custom id so doesn't conflict with
# create form!
# fields_dict = {field.name: django_filters.DateFromToRangeFilter(
#     widget=django_filters.widgets.RangeWidget(attrs={
#         'class': css_date_class,
#         'placeholder': 'dd/mm/yyyy',
#         'id': 'filter_date_{}'.format(i)}),
#     field_name=field.name)
#     for i, field in enumerate(model_fields) if type(field) in dateRangeFields}


# [fields_dict.update({field.name: django_filters.NumericRangeFilter()}) for field in model_fields if field_is_numeric(field)]
#     '{}__lt'.format(field.name): django_filters.NumberFilter(field_name=field.name, lookup_expr='lt'),
#     '{}__gt'.format(field.name): django_filters.NumberFilter(field_name=field.name, lookup_expr='gt')
# })
# BOOLEAN_CHOICES = (('---', ''), ('Yes', 'False'), ('No', 'True'))

# [fields_dict.update(
#     {field.name: django_filters.BooleanFilter(widget=FriendlyBooleanWidget())})
#     for field in model_fields if type(field) == models.BooleanField
# ]
#
# [fields_dict.update(
#     {field.name: django_filters.MultipleChoiceFilter(choices=(('pls',ugettext_lazy('hello'),('a', ugettext_lazy('pls')))))})
#     for field in model_fields if type(field) == models.CharField
# ]


# # custom initialisation function - add css class for DateField types
# def form_init(self, *args, **kwargs):
#
#     # call super first to initialise fields
#     super(type(self), self).__init__(*args, **kwargs)
#
#     def assign_date_class(widget):
#         widget = forms.DateInput(attrs={'class':'css_date_class'})
#
#     print(self.fields)
#     [assign_date_class(f.widget) for f in self.fields if type(f) == DateField]

# #
# def update_object(view, form):
#     if form.is_valid():
#         o = get_object_or_404(view.model)
#         o.save()
#         server_logger.info('{} updated'.format(o))
#         s = True
#     else:
#         server_logger.error('Update failed: {}'.format(errors_string(form)))
#         s = False


# # get context variables for standard template html form - must pass class model. if log_update is 'log_info' highlight
# # first log line in green, if is 'log_error' highlight in red else do nothing see template/log.html for code
# def get_context_vars(model, post_url, log_update, objects):
#     return {
#         'model_class': model, # model class type
#         'model_attributes': model.attributes_table, # get attribute names from class method (must contain the method!)
#         'model_objects': objects, # get objects, with specified order by parameter
#         'form': form_classes[model], # get form for posting new object
#         'post_url': post_url, # url for website to post to
#         'log_update': log_update, # string to indicate whether a post was successful
#         'log_lines': get_log_recent(), # get log from log info file
#     }
# def construct_table_urls(cls):
#     return (
#         path(
#             route=viewname(cls),
#             view=view_table,
#             name=viewname(cls),
#             kwargs={'cls':cls}),
#         path(
#             route='{}/<str:log_update>'.format(viewname(cls)),
#             view=view_table_update,
#             name=viewname_update(cls),
#             kwargs={'cls':cls}),
#         path(
#             route=viewname_new(cls),
#             view=new_object,
#             name=viewname_new(cls),
#             kwargs={'class_type':cls}
#         )
#     )

    # # sites
    # re_path(r'^sites/?$', views_classes.sites, name='sites'),
    # path('sites/<str:log_update>', views_classes.sites_update, name='sites_update'), # has site update
    # path('newsite', posts.new_site, name='newsite'), # posted data
    #
    # # bets
    # re_path(r'^bets/?$', views_classes.bets, name='bets'),
    # path('sites/<str:log_update>', views_classes.bets_update, name='bets_update'), # has bet update
    # path('newbet', posts.bets_update, name='newbet'), # posted data


    # transactions
#     re_path(r'^transactions/?$', views_classes.transactions, name='transactions'),
#     path('transactions/<str:log_update>', views_classes.transactions_update, name='transactions_update'), # has log update
#     path('newtransaction', posts.new_transaction, name='newtransaction'), # posted data
# ]

# remember path uses regular expressions to match
#   ^ - start of string
#   $ - end of string
#   (...) - group
#   ? - 0 or 1 repetitions
#   + - 1 or more repetitions
#   w - string

# # create form instance from class type and post data
# def create_form(cls, post):
#     # create form class
#     Form = form_classes([cls])
#     # create form form posted data
#     return Form(post)

# # *** default functions for view names when updating/creating new ***
# def _vn_update(str, success):
#     return '{}update/{}'.format(str, 'success' if success else 'fail')
#
# # *** conversion funtions from class to view ***
# def viewname(cls):
#     return cls._meta.verbose_name
#
# def viewname_update(cls):
#     return _vn_update(viewname(cls))
#
#
#
# # *** view names including app names ***
# def viewname_full(cls):
#     return '{}:{}'.format(BetlogConfig.name, viewname(cls))
#
# def viewname_full_update(cls):
#     return _vn_update(viewname_full(cls))
#
# def viewname_full_new(cls):
#     return _vn_new(viewname_full(cls))


# get context variables for standard template html form - must pass class model. if log_update is 'log_info' highlight
# first log line in green, if is 'log_error' highlight in red else do nothing see template/log.html for code
# def get_context_vars(model, post_url, log_update, objects):
#     return {
#         'model_class': model, # model class type
#         'model_attributes': model.attributes_table, # get attribute names from class method (must contain the method!)
#         'model_objects': objects, # get objects, with specified order by parameter
#         'form': form_classes[model], # get form for posting new object
#         'post_url': post_url, # url for website to post to
#         'log_update': log_update, # string to indicate whether a post was successful
#         'log_lines': get_log_recent(), # get log from log info file
#     }
#
#
# # view in standard table view with a log update
# def view_table_update(request, cls, log_update):
#
#     # create context variables dictionary
#     contextVars = get_context_vars(
#         model=cls,
#         post_url=viewname_full_new(cls),
#         log_update=log_update,
#         objects=cls.objects.all() # TODO update with ordering
#     )
#
#     # pass variables to table view html template
#     return render(request, 'tableview.html', contextVars)
#
#
# # view in standard table view
# def view_table(request, cls):
#     # wrapper for update function - pass empty log_update so log.html template does not interpret any update
#     return view_table_update(request, cls, '')
#
#
# # default view is list of sites
# def view_default(request):
#     return view_table(request, Site)

#
# # **************************************************** Sites ***********************************************************
# # list of sites with updated log
# def sites_update(request, log_update):
#
#     # create context variables dictionary
#     contextVars = get_context_vars(Site, 'betlog:newsite', log_update, 'name' )
#
#     # pass variables to tableview.html template for rendering
#     return render(request, 'tableview.html', contextVars)
#
# # list of sites - default
# def sites(request):
#     return sites_update(request, '')
#
# # view transactions for a specific site
# def sitelog(request):
#     pass
#
#
# # # **************************************************** Transactions ****************************************************
# # # List of all transactions - updated log
# # def transactions_update(request, log_update):
# #
# #     # create context variables for template
# #     contextVars = get_context_vars(Transaction, 'betlog:newtransaction', log_update, '-date')
# #
# #     # pass context variables to transactions.html template for rendering
# #     return render(request, 'transactions.html', contextVars)
# #
# # def transactions(request):
# #     return transactions_update(request, ' ')
# #
# #
# # # **************************************************** Bets ************************************************************
# # def bets(request):
# #     pass
# # determine if dictionary contains all attributes
# def attributes_exist(attrs, data):
#     return all([name in data for name in attrs])
#
# check to see if any object has an attribute with a specific value
# def element_exists(model, attribute, value):
#     return any([True for obj in model.objects.all() if getattr(obj, attribute) == value])
#
# check if object with specified id exists
# def object_exists(cls, id):
#     return cls.objects.filter(id=id).exists()

# # user has requested to create a new betting site
# def new_site(request):
#
#     form = create_form(Site, request.POST)
#
#     if form.is_valid():
#         s = Site(**form.cleaned_data)
#         s.save()
#         server_logger.info('New site "{}" added'.format(s))
#         return redirect_with_log('sites_update', True)
#     else:
#         server_logger.error('New site failed: {}'.format(errors_string(form)))
#         return redirect_with_log('sites_update', False)
#
#
# #user has requested to create a new transation
# def new_transaction(request):
#
#     form = create_form(Transaction, request.POST)
#
#     if form.is_valid():
#         t = Transaction(**form.cleaned_data)
#         t.save()
#         server_logger.info('New transaction "{}" added.'.format(t))
#         return redirect_with_log('transactions_update', True)
#     else:
#         server_logger.error('New transaction failed: {}.'.format(errors_string(form)))
#         return redirect_with_log('transactions_update', False)
# # new site form
# class SiteForm(ModelForm):
#     class Meta:
#         model = Site
#         fields = ['name', 'comment'] # dont want to give the user the option to enter
#
# # new transaction form
# class TransactionForm(ModelForm):
#     class Meta:
#         model = Transaction
#         fields = Transaction.all_fields

# # easy function for redirecting to transactions page
# def redirect_with_log(cls, success):
#     # log_info tells log.html to display most recent message in green, log_error in red
#     log_urlmsg = 'log_info' if success else 'log_error'
#
#     viewname = viewname_full_update(cls)
#     return HttpResponseRedirect(reverse(viewname, kwargs={'log_update':log_urlmsg}))
# @register.filter
# def is_numeric(cls, attr):
#     mdl = cls._meta.get_field(attr)
#     numericFields = [models.IntegerField, models.DecimalField, models.FloatField]
#     return any([type(mdl) == n for n in numericFields])

# @register.simple_tag
# def get_objects(cls): #get object list - newest first
#     # I dont know why but an instance of Site is passed to template instead of class type?
#     if hasattr(cls, 'date'):
#         return type(cls).objects.order_by('-date')
#     elif hasattr(cls, 'name'):
#         return type(cls).objects.order_by('name')
#     else:
#         return type(cls).objects.all()

# @register.simple_tag
# def get_options(cls, attr):
#     v = getattr(type(cls), attr)
#     if hasattr(v, 'get_queryset'):
#         return v.get_queryset()
#     else:
#         return None

# def _clean(self):
#     print('pls')
#     super(type(self), self).clean()
#     data = self.cleaned_data
#     print('pls')
#     dt_fields = [k for k,v in self.Meta.widgets if v==forms.SplitDateTimeWidget]
#     for dt_field in dt_fields:
#         date_field = '{}_0'.format(dt_field)
#         time_field = '{}_1'.format(dt_field)
#         if any([f not in data for f in [date_field, time_field]]):
#             self.add_error('Expecting date "{}" and time "{}" split fields'.format(date_field, time_field))
#             return
#         data[dt_field] = ' '.join(date_field, time_field)
#         data.pop(date_field)
#         data.pop(time_field)

# # get field friendly view names
# commonFieldTitles = [f.verbose_name for f in commonFields]
#
# # order by date so make sure field exists
# assert('date' in commonFields)
#
# class SiteLogView(TemplateView):
#
#     t_filter_cls = create_fitler(Transaction, view_name)
#     b_filter_cls = create_fitler(Bet, view_name)
#
#     object_fields = ('typeName', *commonFields)
#     field_titles = ('Type', *[get_field_name(Transaction, f) for f in commonFields])
#     view_name = 'Sitelog'
#     template_name = 'default.html'
#
#     # get queryset data from Transaction and bet
#     def get_queryset(self):
#
#         qt_dict = {}
#         # get transaction query set - annotate transactionType.name to 'typeName'
#         qst = Transaction._default_manager.annotate(typeName=F('transactionType__name'))
#
#         # get bet query set - annotate betType.name to 'typeName'
#         qsb = Bet._default_manager.annotate(typeName=F('betType__name'))
#
#         # return querysets joined together
#         return list(chain(qst, qsb)).order_by('-date')
#
#     def get_context_data(self, **kwargs):
#
#         # get transaction query set - annotate transactionType.name to 'typeName'
#         qst = Transaction._default_manager.annotate(typeName=F('transactionType__name'))
#
#         # get bet query set - annotate betType.name to 'typeName'
#         qsb = Bet._default_manager.annotate(typeName=F('betType__name'))
#
#         context=super().get_context_data(**kwargs)
#
#         #context['object_list'] = list(chain(qs1, qs2))
#         context['title'] = 'Site Log'
#         return context
#
#     def get(self, request, *args, **kwargs):
#
#         self.filter = self.f


