"""Shared helpers of the API: permission checks and object access."""

# Standard Library
from typing import TypeVar

# Django
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# Alliance Auth
from allianceauth.authentication.models import User

# AA Example
from example.managers.general import AccessManager, GeneralManager

T = TypeVar("T", bound=models.Model)


def can_view_overview(user: User) -> bool:
    """Check if the user may view the overview pages of the app."""
    return GeneralManager.has_basic_access(user)


def get_object_with_access(
    request, manager: AccessManager[T], manage: bool = False, **lookup
) -> tuple[bool, T | None]:
    """
    Get one object through an `AccessManager` and check the user's access to it.

    Args:
        request: Django Request Object
        manager: The manager of the model, e.g. `CharacterOwner.objects`
        manage: Check against `manage_to` instead of `visible_to` (for write actions)
        **lookup: Lookup of the object, e.g. `character__character_id=1`
    Returns:
        Tuple of (has_permissions: bool, object | None)
    """
    try:
        obj = manager.get(**lookup)
    except ObjectDoesNotExist:
        return False, None

    if manage:
        allowed = manager.manage_to(request.user)
    else:
        allowed = manager.visible_to(request.user)
    return allowed.filter(pk=obj.pk).exists(), obj
