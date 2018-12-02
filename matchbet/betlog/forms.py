from django.forms.models import ModelForm
from django.db.models import Model, Q, DateField, DateTimeField, ForeignKey
from django import forms
from django.utils import timezone

from .models import Transaction, Bet, Site, Match, fieldnames_editable, fields_all
from .widgets import DateTimeWidget, date_input, MySelectorWidget_NoClear


# Negate numeric field if another (type) field requiers it
# e.g. for a transaction a deposit is positive, withdrawal is negative
#
# [form] is input form to pass.
# [numeric_field] is field containing numeric value
# [cls] is of type models.ForeignKey[cls] - specifies model sub-type and must be contained within the form
# [filter_negatives] - filter_instances applied to [cls]. checked against to see if negation is required
def negate_field(form, numeric_field, cls_name, filter_negatives):
    # first check number value inputted isn't negative
    if form.cleaned_data[numeric_field] < 0:
        form.add_error(numeric_field, 'Input value must be greater than 0 (server handles negation).')
        return

    # get class type instance
    cls = form.cleaned_data[cls_name]

    # get class type which require negation
    cls_negatives = type(cls).objects.filter(filter_negatives)

    # check if class matches any of the types that require negative
    if any([cls == t for t in cls_negatives]):
        form.cleaned_data[numeric_field] = abs(form.cleaned_data[numeric_field]) * -1



# return dictionary mapping of fields to custom widgets
def formatted_fields(field_list):

    w_dict = {
        DateTimeField: lambda field: forms.DateTimeField(widget=DateTimeWidget(), initial=timezone.now),
        DateField: lambda field:    forms.DateField(widget=date_input(), initial=timezone.now),
    }

    return {f.name:w_dict[type(f)](f) for f in field_list if type(f) in w_dict}


# dictionary of model type: fields to display absolute value
absFields = {Transaction: ('balanceAdjust',), Bet: ('balanceAdjust',)}

# set numeric fields to absolute value (where required)
def form_init(self, *args, **kwargs):

    # call class super initialisation
    ModelForm.__init__(self, *args, **kwargs)

    # check model is in dictionary
    if self.Meta.model in absFields:

        # get fields specific to this model
        fieldsDict = absFields[self.Meta.model]

        # if field is in required list of absolutes set absolute value in dict
        newValues = {f: abs(getattr(self.instance, f)) for f in self.Meta.fields if f in fieldsDict}

        # update initial dict
        self.initial.update(newValues)

def create_form_type(model_type: Model, custom_fields=None) -> ModelForm:

    # set custom fields to empty dictionary if unused to prevent None errors
    custom_fields = custom_fields or {}

    # set form python name
    form_name = 'Form_{}'.format(model_type.__name__)

    # get editable fields
    field_names = fieldnames_editable(model_type)

    class Meta:
        model = model_type # required for form instansation
        fields = field_names
        widgets = {
            f.name: MySelectorWidget_NoClear
            for f in fields_all(model_type)
            if type(f) == ForeignKey and f.name not in custom_fields
        }

    # create class dictionary - has Meta class and initialisation
    cls_dict = {'Meta': Meta, '__init__':form_init}

    # update class dictionary with customised field instances
    cls_dict.update(formatted_fields(fields_all(model_type)))

    # update with custom inputted fields
    cls_dict.update(custom_fields)

    cls = type(form_name, (ModelForm,), cls_dict)
    return cls


# custom form clean() func for Transaction model - negate balance adjustment of transaction types 'Withdraw' and 'Fee' transactions
def transaction_clean(self):
    super(type(self), self).clean()
    if self.is_valid():
        negate_field(
            self,
            'balanceAdjust',
            'transactionType',
             Q(name='Withdraw') | Q(name='Fee'))

# custom form clean() func for Bet model - only bet type to not negate balance adjustment is 'Win'
def bet_clean(self):
    super(type(self), self).clean()
    if self.is_valid():
        negate_field(
            self,
            'balanceAdjust',
            'betType',
            ~Q(name='Win')
        )

# dictionary of form_classes, where class type is key, returns form class
TransactionForm = create_form_type(Transaction)
TransactionForm.clean = transaction_clean

SiteForm = create_form_type(Site)
MatchForm = create_form_type(Match)

BetForm = create_form_type(Bet)
BetForm.clean = bet_clean

form_classes = {Site: SiteForm, Transaction: TransactionForm, Match: MatchForm, Bet: BetForm}