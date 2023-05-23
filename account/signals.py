from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import Account


@receiver(post_save, sender=Account, dispatch_uid="confirm_email")
def create_acc_after_email(sender, instance, created, *args, **kwargs):
    if created:
        print("Sending email to user about ")
