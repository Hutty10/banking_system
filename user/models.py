import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from user.constants import Gender, Title
from user.managers import UserManager

# Create your models here.


class User(PermissionsMixin, AbstractBaseUser):
    id = models.UUIDField(
        _("ID"),
        editable=False,
        unique=True,
        primary_key=True,
        default=uuid.uuid4,
        db_index=True,
    )
    email = models.EmailField(_("Email"), max_length=254, db_index=True, unique=True)
    title = models.CharField(_("Title"), max_length=7, choices=Title.choices)
    first_name = models.CharField(_("First Name"), max_length=20)
    last_name = models.CharField(_("Last Name"), max_length=20)
    middle_name = models.CharField(_("Middle Name"), max_length=20)
    gender = models.CharField(_("Gender"), max_length=12, choices=Gender.choices)
    phone = models.CharField(_("Phone Number"), max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(_("Date Created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date Updated"), auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def fullname(self) -> str:
        if self.middle_name:
            return f"{self.title} {self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.title} {self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.fullname

    def tokens(self) -> dict:
        tokens = RefreshToken.for_user(self)
        return {"refresh": str(tokens), "access": str(tokens.access_token)}

class UserAddress(models.Model):
    user = models.OneToOneField(
        User,
        related_name='address',
        on_delete=models.CASCADE,
    )
    street_address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    postal_code = models.PositiveIntegerField()
    country = models.CharField(max_length=256)

    def __str__(self):
        return self.user.email