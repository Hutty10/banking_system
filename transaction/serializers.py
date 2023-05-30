from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from account.models import Account
from transaction.constants import TransactionTypeChoices
from transaction.models import Transactions


class TransactionSerializer(serializers.ModelSerializer):
    # account = serializers.SerializerMethodField()
    # # ammount =

    # def get_account(self, obj):
    #     import pdb

    #     pdb.set_trace()
    #     return Account.objects.get(obj)

    class Meta:
        model = Transactions
        fields = [
            "id",
            "amount",
            "account",
            "receiver_account",
            "transaction_type",
            "description",
            "created_at",
            "updated_at",
        ]

    extra_kwargs = {
        "id": {"read_only": True},
        "transaction_type": {"read_only": True},
        "created_at": {"read_only": True},
        "updated_at": {"write_only": True},
    }

    def validate(self, attrs):
        context = self.context
        transaction_type = context.get("transaction_type")
        amount = attrs.get("amount")
        # print(amount)
        # account = attrs.get("account")
        # print(attrs)
        # print(account)
        # import pdb

        # pdb.set_trace()
        is_deposit = transaction_type == TransactionTypeChoices.DEPOSIT
        is_withdraw = transaction_type == TransactionTypeChoices.WITHDRAW
        is_transfer = transaction_type == TransactionTypeChoices.TRANSFER
        if is_deposit and amount < settings.MINIMUM_DEPOSIT_AMOUNT:
            raise serializers.ValidationError(
                f"You need to deposit at least {settings.MINIMUM_DEPOSIT_AMOUNT} "
            )
        if is_withdraw:
            account = context.get("account")
            print(f"acc--{account}")
            account = Account.objects.get(account_no=account)
            balance = account.balance
            min_withdraw_amount = settings.MINIMUM_WITHDRAWAL_AMOUNT
            max_withdraw_amount = account.account_type.maximum_withdrawal_amount
            if amount < min_withdraw_amount:
                raise serializers.ValidationError(
                    f"You can withdraw at least {min_withdraw_amount} "
                )

            if amount > max_withdraw_amount:
                raise serializers.ValidationError(
                    f"You can withdraw at most {max_withdraw_amount} "
                )

            if amount > balance:
                raise serializers.ValidationError(
                    f"Insufficient Fund\nYou have {balance}  in your account. "
                )

        if is_transfer:
            if not context.get("receiver_account"):
                raise serializers.ValidationError("receiver_account field required")
            account = context.get("account")
            account = Account.objects.get(account_no=account)
            balance = account.balance
            min_transfer_amount = settings.MINIMUM_TRANSFER_AMOUNT

            if amount > balance:
                raise serializers.ValidationError(
                    f"Insufficient Fund\nYou have {balance}  in your account. "
                )
            if amount < min_transfer_amount:
                raise serializers.ValidationError(
                    f"You can transfer at least {min_transfer_amount} "
                )

        return super().validate(attrs)

    def create(self, validated_data):
        return super().create(validated_data)
