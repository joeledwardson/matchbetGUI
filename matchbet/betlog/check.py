from .models import TransactionType, BetType
from functools import reduce
import operator
from django.db.models import Q
from .names import model_viewname

model_types = {
    TransactionType: ['Deposit', 'Withdraw', 'Fee'],
    BetType: ['Lay bet', 'Back bet', 'Win', 'Loss']}

def new_model(model_type, name):
    model_type(name=name).save()
    print('"{}" not found in "{}" db - added.'.format(name, model_viewname(model_type)))

for mdl, names in model_types.items():
    [new_model(mdl, nm) for nm in names if not mdl.objects.filter(name=nm)]

    # reduce performs function sequentially on all pairs
    # operator.and_ is bitwise and
    # filter to remaining objects not corresponding to dict names
    f = reduce(operator.and_, (~Q(name=nm) for nm in names))
    extras = mdl.objects.filter(f)

    print_warning = lambda m: print('"{}" not found in "{}" list - consider deleting..'.format(m, model_viewname(mdl)))
    list(map(print_warning, extras))

print('done')