from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from user.views import (
    LoginView,
    PasswordTokenCheckView,
    RegisterView,
    RequestPasswordResetView,
    SetNewPasswordView,
    UserView,
    VerifyEmailView,
)

app_name = "user"

urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "email-verify/<slug:uidb64>/<slug:token>/",
        VerifyEmailView.as_view(),
        name="email_verify",
    ),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "request-reset-email/",
        RequestPasswordResetView.as_view(),
        name="request-reset-email",
    ),
    path(
        "password-check/<uidb64>/<token>/",
        PasswordTokenCheckView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset-complete/",
        SetNewPasswordView.as_view(),
        name="password-reset-complete",
    ),
    path(
        "<uuid:pk>/",
        UserView.as_view(),
        name="user-detail",
    ),
]
