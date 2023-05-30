from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.utils import timezone
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

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
        response = {
            "message": "DEPOSIT successful",
            "data": {
                "account": account.account_no,
                "amount": Decimal(serializer.data.get("amount")),
                "balance": account.balance,
            },
            "status": True,
            "status_code": HTTP_200_OK,
        }
        return Response(response, status=HTTP_200_OK)


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
        response = {
            "message": "WITHDRAW successful",
            "data": {
                "account": account.account_no,
                "amount": Decimal(serializer.data.get("amount")),
                "balance": account.balance,
            },
            "status": True,
            "status_code": HTTP_200_OK,
        }
        return Response(response, status=HTTP_200_OK)


class TransferMoneyView(TransactionCreateMixin):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(
            data=data,
            context={
                "transaction_type": TransactionTypeChoices.TRANSFER,
                "account": data.get("account"),
                "receiver_account": data.get("receiver_account"),
            },
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
        response = {
            "message": "TRANSFER successful",
            "data": {
                "sender": source_account.account_no,
                "receiver": receiver_account.account_no,
                "amount": Decimal(serializer.data.get("amount")),
                "balance": source_account.balance,
            },
            "status": True,
            "status_code": HTTP_200_OK,
        }
        return Response(response, status=HTTP_200_OK)
