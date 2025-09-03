"""Models for Example."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from esi.models import Token

# AA Example
from example.managers import ExampleManager


class General(models.Model):
    """General model for app permissions"""

    class Meta:
        managed = False
        permissions = (
            ("basic_access", _("Can access this app, Example")),
            ("manage_access", _("Can manage Example")),
        )
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
        default_permissions = ()  # Remove standard permissions

    def __str__(self):
        return f"{self.token.character_name} - {self.token.character_id}"

    objects = ExampleManager()
