# Generated by Django 4.2 on 2023-05-01 16:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AccountType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[("savings", "savings"), ("current", "current")],
                        max_length=20,
                        verbose_name="Account type",
                    ),
                ),
                (
                    "maximum_withdrawal_amount",
                    models.DecimalField(decimal_places=2, max_digits=12),
                ),
                (
                    "annual_interest_rate",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Interest rate from 0 - 100",
                        max_digits=5,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                    ),
                ),
                (
                    "interest_calculation_per_year",
                    models.PositiveSmallIntegerField(
                        help_text="The number of times interest will be calculated per year",
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(12),
                        ],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("account_no", models.BigIntegerField(blank=True, unique=True)),
                (
                    "balance",
                    models.DecimalField(decimal_places=2, default=0, max_digits=12),
                ),
                (
                    "interest_start_date",
                    models.DateField(
                        blank=True,
                        help_text="The month number that interest calculation will start from",
                        null=True,
                    ),
                ),
                ("initial_deposit_date", models.DateField(blank=True, null=True)),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Date Updated"),
                ),
                (
                    "account_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="accounts",
                        to="account.accounttype",
                    ),
                ),
            ],
        ),
    ]
