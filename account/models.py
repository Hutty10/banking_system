from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from account.constants import AccountTypeChoices
from user.models import User

# Create your models here.


class AccountType(models.Model):
    name = models.CharField(
        _("Account type"),
        max_length=20,
        choices=AccountTypeChoices.choices,
        unique=True,
    )
    maximum_withdrawal_amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        db_index=True,
    )
    annual_interest_rate = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        decimal_places=2,
        max_digits=5,
        help_text="Interest rate from 0 - 100",
    )
    interest_calculation_per_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="The number of times interest will be calculated per year",
    )

    @classmethod
    def calculate_interest(self, principal):
        """
        Calculate interest for each account type.

        This uses a basic interest calculation formula
        """
        p = principal
        r = self.annual_interest_rate
        n = Decimal(self.interest_calculation_per_year)

        # Basic Future Value formula to calculate interest
        interest = (p * (1 + ((r / 100) / n))) - p

        return round(interest, 2)

    def __str__(self):
        return self.name


class Account(models.Model):
    user = models.OneToOneField(
        User,
        related_name="account",
        on_delete=models.CASCADE,
    )
    account_type = models.ForeignKey(
        AccountType, related_name="accounts", on_delete=models.CASCADE
    )
    account_no = models.CharField(
        unique=True, blank=True, max_length=10, editable=False
    )
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    interest_start_date = models.DateField(
        null=True,
        blank=True,
        help_text=("The month number that interest calculation will start from"),
    )
    initial_deposit_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date Updated"), auto_now=True)

    def __str__(self):
        return str(self.account_no)

    def get_interest_calculation_months(self):
        """
        List of month numbers for which the interest will be calculated

        returns [2, 4, 6, 8, 10, 12] for every 2 months interval
        """
        interval = int(12 / self.account_type.interest_calculation_per_year)
        start = self.interest_start_date.month
        return [i for i in range(start, 13, interval)]
