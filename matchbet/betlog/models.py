from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

from moneyed.localization import format_money
from moneyed import Money

# field that holds UK currency
class MyMoneyField(models.DecimalField):
    @staticmethod
    def money_str(amount):
        return format_money(Money(amount, 'GBP'), locale='en_GB')

# formate just date from datetimefield or datefield
date_format = lambda date: date.date().strftime('%d %b %y')

# return all fields (not id, or any auto incrementing fields)
# get all editable field names not id, (or any auto incrementing fields)
# if type(f) is not models.fields.AutoField
is_pk = lambda f, m: f == m._meta.pk
is_currency = lambda f: type(f) == MyMoneyField

fields_all = lambda model: [f for f in model._meta.fields if not is_pk(f, model)]
fields_editable = lambda model: [f for f in fields_all(model) if f.editable]
fieldnames_all = lambda model: [f.name for f in fields_all(model)]
fieldnames_editable = lambda model: [f.name for f in fields_editable(model)]


# *************************************************** Types ************************************************************
class ModelType(models.Model):
    name = models.CharField(max_length=255,
                            unique=True,
                            blank=False)
    def __str__(self):
        return self.name
    class Meta:
        abstract = True

class TransactionType(ModelType):
    pass

class BetType(ModelType):
    pass


# *************************************************** Websites *********************************************************
# Top level sites table - holds data about each url
class Site(models.Model):

    # name of website - want each name to be unique
    name = models.CharField(max_length=30,
                            verbose_name="Name",
                            blank=False,
                            unique=True,
                            validators=[RegexValidator(
                                regex=r'[a-zA-Z0-9 ]+',
                                message='Please enter a valid character or space'
                            )])

    # current balance - dependent on transactions
    balance = MyMoneyField(default=0,
                         max_digits=14,
                         decimal_places=2,
                         verbose_name='Balance',
                         editable=False)


    def __str__(self):
        return self.name

    # update site balance
    def update_balance(self, adjustment):
        self.balance += adjustment
        self.save()

    # re-calculate site balance from list of transactions
    def calculate_balance(self):
        self.balance = sum([t.balanceAdjust for t in Transaction.objects.filter(site=self)])
        self.balance += sum([b.balanceAdjust for b in Bet.objects.filter(site=self)])
        self.save()


# Abstract class which alters the balance of a site
class SiteExchange(models.Model):

    class Meta:
        abstract = True

    # site in which bet is placed
    site = models.ForeignKey(Site,
                             on_delete=models.CASCADE,
                             verbose_name="Site")

    # amount to change site balance
    balanceAdjust = MyMoneyField(
        max_digits=7,
        decimal_places=2,
        blank=False,
        default=5.0,
        verbose_name="Balance Adjust")

    # date of balance change
    date = models.DateTimeField(default=timezone.now,
                                verbose_name="Date",
                                blank=False)


# **************************************************** Matches *********************************************************
# Betting matches
class Match(models.Model):
    team1 = models.CharField(max_length=20,
                             verbose_name="Team 1",
                             blank=False)

    team2 = models.CharField(max_length=20,
                             verbose_name="Team 2",
                             blank=False)

    date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date Complete")


    # e.g. arsenal vs tottenham on 12/10/2018
    def __str__(self):
        return '{} vs {} {}'.format(
            self.team1,
            self.team2,
            date_format(self.date))

    class Meta:
        verbose_name_plural = 'Matches'


# ************************************************* Bets ***************************************************************
# Bet class
class Bet(SiteExchange):

    # type of bet
    betType = models.ForeignKey(BetType,
                                on_delete=models.CASCADE,
                                verbose_name="Type")

    # corresponding match bet is placed
    match = models.ForeignKey(Match,
                              on_delete=models.CASCADE,
                              verbose_name="Match")

    # descrption of bet - e.g. arsenal to win
    description = models.CharField(verbose_name='Description',
                                   max_length=255,
                                   blank=True)

    # e.g. Lay bet 10 on Williamshill, arsenal vs chelsea on 12/10/2018
    def __str__(self):
        return '{} {} on {}, {}'.format(
            self.betType,
            MyMoneyField.money_str(abs(self.balanceAdjust)),
            self.site,
            self.match)

# ******************************************************* Transactions *************************************************
# Transaction - transfer money to or from Site
class Transaction(SiteExchange):

    # transaction type
    transactionType = models.ForeignKey(
        TransactionType,
        on_delete=models.CASCADE,
        verbose_name="Type")

    # e.g. Desposit £10 to Bet365
    def __str__(self):
        return "Site {}: {} {}".format(
            self.site,
            self.transactionType,
            MyMoneyField.money_str(abs(self.balanceAdjust)))
