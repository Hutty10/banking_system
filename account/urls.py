from django.urls import path
from account.views import AccountDetailView, AccountView

app_name = "account"

urlpatterns = [
    path("", AccountView.as_view(), name="account_list"),
    path("<int:pk>/", AccountDetailView.as_view(), name="account_detail"),
]
