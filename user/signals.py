from django.contrib.sites.shortcuts import get_current_site
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from user.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from user.utils import activation_token, Utils


@receiver(post_save, sender=User, dispatch_uid="confirm_email")
def send_confiremation_email(sender, instance, created, **kwargs):
    if created:
        try:
            data = {
                "to_email": instance.email,
                "email_subject": "Confirm Your Email Address",
                "email_body": render_to_string(
                    "account/registration/account_activation_email.html",
                    {
                        "first_name": instance.first_name,
                        "domain": get_current_site(sender).domain,
                        "uid": urlsafe_base64_encode(force_bytes(instance.pk)),
                        "token": activation_token.make_token(instance),
                    },
                ),
            }
            Utils.send_email(data)
        except Exception as e:
            print(f"error sending confirmation: {e}")
    pass
