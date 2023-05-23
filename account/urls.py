from django.urls import path
from account.views import AccountCreateView, AccountDetailView

app_name = "account"

urlpatterns = [
    path("create/", AccountCreateView.as_view(), name="account_create"),
    path("<str:account_no>/", AccountDetailView.as_view(), name="account_detail"),
]
