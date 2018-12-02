from django.db.models import F, CharField

from betlog.models import TransactionType, BetType
from betlog.models import Transaction, Bet, fieldnames_all, fields_all, Site

# custom view name - normally based on model
sitelog_view_name = 'sitelog'
# variable name which holds site name - used in url configuration
sitelog_site_var = 'viewsite'

# models used by sitelog are transactions and bets
models = [Transaction, Bet]

# 'Type' field names in models
typeFields = {
    Transaction: 'transactionType',
    Bet: 'betType',
}

# site foreign key field name for transaction/bet
siteFieldName = 'site'

# create 'type' values for filter
type_values = lambda type_model: [
    (v.name, v.name) for v in type_model._default_manager.all()
]

# object 'type' field - concatenates transaction type and bet type
objectType = CharField(
    max_length=255,
    blank=True,
    name='object_type', # must use one of the field types to get filter to print 'Type'
    verbose_name='Type',
    choices=[
        ['Transaction', tuple(type_values(TransactionType))],
        ['Bet', tuple(type_values(BetType))]
    ]
)

# first field is object 'type'
fields = [objectType]

# get all fields common between Bet and Transaction - (filter to specific site)
fields += [
    f for f in fields_all(Transaction)
    if f.name in fieldnames_all(Bet) and
    f.related_model is not Site
]