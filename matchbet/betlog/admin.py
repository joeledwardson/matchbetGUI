from django.contrib import admin

from .models import Site, Match, TransactionType, BetType, Bet, Transaction

# Register your models here.
admin.site.register(Site)
admin.site.register(Match)
admin.site.register(TransactionType)
admin.site.register(BetType)
admin.site.register(Bet)
admin.site.register(Transaction)
