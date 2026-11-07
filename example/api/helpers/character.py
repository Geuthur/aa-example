"""Helpers of the character API."""

# AA Example
from example.api.helpers.core import get_object_with_access
from example.models.character import CharacterOwner


def get_character_owner(
    request, character_id: int, manage: bool = False
) -> tuple[bool, CharacterOwner | None]:
    """
    Get a CharacterOwner by EVE character id and check permissions.

    Args:
        request: Django Request Object
        character_id: EVE character ID of the owner
        manage: Check against `manage_to` instead of `visible_to` (for write actions)
    Returns:
        Tuple of (has_permissions: bool, CharacterOwner | None)
    """
    return get_object_with_access(
        request,
        CharacterOwner.objects,
        manage=manage,
        character__character_id=character_id,
    )
