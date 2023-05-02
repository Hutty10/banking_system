from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

class AccountTypeChoices(TextChoices):
    SAVINGS = "savings", _("savings")
    CURRENT = "current", _("current")