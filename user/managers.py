from typing import Any

from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        first_name,
        last_name,
        password=None,
        **extra_fields,
    ) -> Any:
        if not first_name:
            raise ValueError(_("User Should have a first_name"))
        if not last_name:
            raise ValueError(_("User Should have a last_name"))
        if not email:
            raise ValueError(_("User Should have an Email"))
        if password is None:
            raise ValueError(_("Password is compulsory"))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        first_name,
        last_name,
        password=None,
        **extra_fields,
    ) -> Any:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("title", 'Admin')
        if not extra_fields.get("is_staff"):
            raise ValueError(_("staff must be set to true"))
        if not extra_fields.get("is_superuser"):
            raise ValueError(_("Superuser must be set to true"))
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            **extra_fields,
        )
        return user
