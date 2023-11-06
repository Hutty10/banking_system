# Generated by Django 4.2 on 2023-11-06 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0002_initial"),
        ("transaction", "0002_alter_transactions_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transactions",
            name="receiver_account",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="receiver",
                to="account.account",
                verbose_name="Receiver account",
            ),
        ),
    ]
