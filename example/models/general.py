"""Models for General."""

# Standard Library
import uuid

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.authentication.models import User

# AA Example
from example.managers.general import GeneralManager


def generate_unique_string(length=12):
    """Generate a unique String"""
    unique_id = str(uuid.uuid4())
    unique_id = unique_id.replace("-", "")
    return unique_id[:length]


class General(models.Model):
    """A model defining the permissions of Example.

    Permissions are checked with Django and the full string, e.g.
    `@permission_required("example.basic_access")` or
    `user.has_perm("example.basic_access")`.
    """

    objects = GeneralManager()

    class Meta:
        abstract = True  # Please Remove this to activate this model
        managed = False
        default_permissions = ()  # Remove standard permissions
        verbose_name = "AA-Example"
        verbose_name_plural = "AA-Example"
        permissions = (
            ("basic_access", _("Can access this app, Example.")),
            ("manage_access", _("Can manage Example.")),
            ("full_access", _("Full access to Example.")),
        )


class UserSettings(models.Model):
    class Meta:
        abstract = True  # Please Remove this to activate this model
        default_permissions = ()  # Remove standard permissions

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="+",
    )

    disable_notifications = models.BooleanField(default=False)
