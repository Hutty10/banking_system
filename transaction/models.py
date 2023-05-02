from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import Account
from transaction.constants import TransactionTypeChoices

# Create your models here.


class Transactions(models.Model):
    account = models.ForeignKey(
        Account,
        verbose_name=_("Account ID"),
        on_delete=models.CASCADE,
    )
    transaction_type = models.CharField(
        _("Transaction type"),
        max_length=50,
        choices=TransactionTypeChoices.choices,
    )
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)
    description = models.TextField(_("Description"))
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date updated"), auto_now=True)
