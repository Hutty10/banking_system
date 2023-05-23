from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import Account
from transaction.constants import TransactionTypeChoices

# Create your models here.


class Transactions(models.Model):
    account = models.ForeignKey(
        Account,
        verbose_name=_("Account"),
        on_delete=models.CASCADE,
        editable=False,
    )
    receiver_account = models.ForeignKey(
        Account,
        verbose_name=_("Receiver account"),
        on_delete=models.CASCADE,
        related_name="receiver",
        editable=False,
        blank=True,
        null=True,
    )
    transaction_type = models.CharField(
        _("Transaction type"),
        max_length=50,
        choices=TransactionTypeChoices.choices,
        blank=True,
    )
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)
    description = models.TextField(_("Description"), blank=True, null=True)
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date updated"), auto_now=True)

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")

    def __str__(self) -> str:
        transaction_type = self.transaction_type
        reference = "to" if transaction_type == "deposit" else "from"
        return f"{transaction_type} - {self.amount} {reference}  {self.account}"
