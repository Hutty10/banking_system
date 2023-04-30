from decouple import config
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from user.models import User
from user.utils import Utils, activation_token


@receiver(post_save, sender=User, dispatch_uid="confirm_email")
def send_confiremation_email(sender, instance, created, *args, **kwargs) -> None:
    if created:
        try:
            data = {
                "to_email": instance.email,
                "email_subject": "Confirm Your Email Address",
                "email_body": render_to_string(
                    "account_activation_email.html",
                    {
                        "first_name": instance.first_name,
                        "domain": config("DOMAIN"),
                        "uid": urlsafe_base64_encode(force_bytes(instance.pk)),
                        "token": activation_token.make_token(instance),
                    },
                ),
            }
            Utils.send_email(data)
        except Exception as e:
            print(f"error sending confirmation: {e}")
