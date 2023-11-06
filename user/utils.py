import threading

from decouple import config
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage, get_connection
from django.http import HttpResponsePermanentRedirect
from six import text_type

# from config.settings import DEFAULT_FROM_EMAIL


class EmailThread(threading.Thread):
    def __init__(self, email) -> None:
        self.email = email
        threading.Thread.__init__(self)

    def run(self) -> None:
        self.email.send()


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)


activation_token = AccountActivationTokenGenerator()


class Utils:
    @staticmethod
    def send_email(data) -> None:
        with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
            use_ssl=settings.EMAIL_USE_SSL,
        ) as connection:
            email = EmailMessage(
                subject=data["email_subject"],
                body=data["email_body"],
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[data["to_email"]],
                connection=connection,
            )
            email.content_subtype = "html"
        EmailThread(email).start()


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [config("APP_SCHEME"), "http", "https"]
