"""Models for Example."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from esi.models import Token

from example.managers import ExampleManager


class General(models.Model):
    """General model for app permissions"""

    class Meta:
        abstract = True  # Please Remove this to activate this model
        managed = False
        permissions = (("basic_access", _("Can access this app")),)
        default_permissions = ()


class Example(models.Model):
    """Example model for app"""

    token = models.ForeignKey(
        Token,
        on_delete=models.CASCADE,
        related_name="example",
        verbose_name=_("Token"),
    )

    class Meta:
        abstract = True  # Please Remove this to activate this model
        managed = False
        verbose_name = _("Example")
        verbose_name_plural = _("Examples")

    def __str__(self):
        return f"{self.token.character_name} - {self.token.character_id}"

    objects = ExampleManager()
