import threading

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from six import text_type

from config.settings import DEFAULT_FROM_EMAIL


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
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            from_email=DEFAULT_FROM_EMAIL,
            to=[data["to_email"]],
        )
        EmailThread(email).start()
