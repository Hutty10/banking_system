from django.urls import path
from transaction.views import DepositMoneyView, WithdrawMoneyView, TransferMoneyView

app_name = "transaction"

urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit"),
    path("withdraw/", WithdrawMoneyView.as_view(), name="withdraw"),
    path("transfer/", TransferMoneyView.as_view(), name="transfer"),
]
