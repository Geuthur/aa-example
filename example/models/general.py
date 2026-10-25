"""Models for General."""

# Standard Library
import uuid
from typing import Any

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.authentication.models import User


def generate_unique_string(length=12):
    """Generate a unique String"""
    unique_id = str(uuid.uuid4())
    unique_id = unique_id.replace("-", "")
    return unique_id[:length]


class General(models.Model):
    """A model defining commonly used properties, permissions, and helper methods for Example."""

    class Permission(models.TextChoices):
        BASIC_ACCESS = "basic_access", _("Can access this app, Example.")
        MANAGE_ACCESS = "manage_access", _("Can manage Example.")
        FULL_ACCESS = "full_access", _("Full access to Example.")

    class Meta:
        abstract = True  # Please Remove this to activate this model
        managed = False
        default_permissions = ()  # Remove standard permissions
        verbose_name = "AA-Example"
        verbose_name_plural = "AA-Example"

    # Inject dynamic permissions
    Meta.permissions = Permission.choices

    @classmethod
    def get_perm(cls, perm: "str | Permission") -> str:
        """Return full permission string 'example.<codename>'."""
        codename = perm.value if isinstance(perm, cls.Permission) else perm
        return f"example.{codename}"

    @classmethod
    def has_perm(cls, user: Any, perm: "str | General.Permission") -> bool:
        """Check if user has permission."""
        if not user or not hasattr(user, "has_perm"):
            return False
        return user.has_perm(cls.get_perm(perm))

    @classmethod
    def has_any_perm(cls, user: Any, *perms: "str | General.Permission") -> bool:
        """Return True if user has any of the specified permissions."""
        if not user or not hasattr(user, "has_perm"):
            return False
        return any(user.has_perm(cls.get_perm(p)) for p in perms)

    @classmethod
    def has_management_access(cls, user: Any) -> bool:
        """Check if user has any management permission."""
        return cls.has_any_perm(
            user,
            cls.Permission.MANAGE_ACCESS,
            cls.Permission.FULL_ACCESS,
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
