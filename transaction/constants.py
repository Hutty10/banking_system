from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class TransactionTypeChoices(TextChoices):
    TRANSFER = "transfer", _("transfer")
    WITHDRAW = "withdraw", _("withdraw")
    DEPOSIT = "deposit", _("deposit")
