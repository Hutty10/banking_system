from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class TitleChoices(TextChoices):
    Mr = "Mr", _("Mr")
    Mrs = "Mrs", _("Mrs")
    Miss = "Miss", _("Miss")
    Doc = "Doc", _("Doc")
    Engr = "Engr", _("Engr")
    Prof = "Prof", _("Prof")

    __empty__ = _("Unknown")


class GenderChoices(TextChoices):
    MALE = "M", _("Male")
    FEMALE = "F", _("Female")

    __empty__ = _("Unknown")
