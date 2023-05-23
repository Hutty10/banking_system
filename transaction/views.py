from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db import transaction
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from account.models import Account
from transaction.constants import TransactionTypeChoices
from transaction.permissions import CanTransact
from transaction.serializers import TransactionSerializer

# Create your views here.


class TransactionCreateMixin(CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [CanTransact]


class DepositMoneyView(TransactionCreateMixin):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(
            data=data,
            context={"transaction_type": TransactionTypeChoices.DEPOSIT},
        )
        serializer.is_valid(raise_exception=True)
        amount = Decimal(data.get("amount"))
        account = Account.objects.get(account_no=data.get("account"))

        if not account.interest_start_date:
            now = timezone.now()
            next_interest_month = int(
                12 / account.account_type.interest_calculation_per_year
            )
            account.initial_deposit_date = now
            account.interest_start_date = now + relativedelta(
                months=+next_interest_month
            )
        account.balance += amount
        account.save(
            update_fields=[
                "initial_deposit_date",
                "balance",
                "interest_start_date",
            ],
        )
        serializer.save(
            account=account, transaction_type=TransactionTypeChoices.DEPOSIT
        )

        return Response(
            {"message": f"{amount} was deposited to {account.account_no} successfully"}
        )


class WithdrawMoneyView(TransactionCreateMixin):
    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = self.serializer_class(
            data=data,
            context={
                "transaction_type": TransactionTypeChoices.WITHDRAW,
                "account": data.get("account"),
            },
        )
        serializer.is_valid(raise_exception=True)
        amount = Decimal(data.get("amount"))
        account = Account.objects.get(account_no=data.get("account"))
        account.balance -= amount
        account.save(update_fields=["balance"])
        serializer.save(
            account=account, transaction_type=TransactionTypeChoices.WITHDRAW
        )
        return Response(
            {"message": f"{amount} was withdraw from {account.account_no} successfully"}
        )


class TransferMoneyView(TransactionCreateMixin):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(
            data=data, context={"transaction_type": TransactionTypeChoices.TRANSFER}
        )
        serializer.is_valid(raise_exception=True)
        amount = Decimal(data.get("amount"))
        source_account = Account.objects.select_for_update().get(
            account_no=data.get("account")
        )
        receiver_account = Account.objects.select_for_update().get(
            account_no=data.get("receiver_account")
        )
        if not receiver_account.interest_start_date:
            now = timezone.now()
            next_interest_month = int(
                12 / receiver_account.account_type.interest_calculation_per_year
            )
            receiver_account.initial_deposit_date = now
            receiver_account.interest_start_date = now + relativedelta(
                months=+next_interest_month
            )
        with transaction.atomic():
            source_account.balance -= amount
            source_account.save(update_fields=["balance"])

            receiver_account.balance += amount
            receiver_account.save(
                update_fields=[
                    "initial_deposit_date",
                    "balance",
                    "interest_start_date",
                ]
            )

        serializer.save(
            account=source_account,
            receiver_account=receiver_account,
            transaction_type=TransactionTypeChoices.TRANSFER,
        )
        return Response(
            {"msg": f"transfered {amount} from {source_account} to {receiver_account}"}
        )
