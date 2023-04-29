from django.urls import path

from user.views import RegisterView,VerifyEmailView

app_name = "user"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path('email-verify', VerifyEmailView.as_view(), name='email_verify')
]
