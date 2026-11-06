"""Character module: an owner model with ESI sections and its update status."""

# Standard Library
from typing import TYPE_CHECKING

# Django
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.functional import cached_property

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter, Token
from esi.errors import TokenError

# AA Example
from example.managers.character import (
    CharacterOwnerManager,
    CharacterUpdateStatusManager,
)
from example.models.helpers.update_manager import (
    CharacterUpdateSection,
    UpdateManagerMixin,
    UpdateSectionResult,
    UpdateStatusBaseModel,
)


class CharacterOwner(UpdateManagerMixin, models.Model):
    """A character that is updated from ESI, section by section."""

    update_section_class = CharacterUpdateSection
    update_status_model = "CharacterUpdateStatus"  # set below, after the class exists

    if TYPE_CHECKING:  # Give type hints for related names
        example_update_status: CharacterUpdateStatusManager

    class Meta:
        default_permissions = ()

    objects: CharacterOwnerManager = CharacterOwnerManager()

    character = models.OneToOneField(
        EveCharacter, on_delete=models.CASCADE, related_name="example_character"
    )
    active = models.BooleanField(default=True)
    wallet_balance = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, default=None
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.character.character_name)

    @classmethod
    def get_esi_scopes(cls) -> list[str]:
        """Return list of required ESI scopes to fetch."""
        return ["esi-wallet.read_character_wallet.v1"]

    def get_token(self) -> Token:
        """Return a valid token of this character with the scopes of the app."""
        token = (
            Token.objects.filter(character_id=self.character.character_id)
            .require_scopes(self.get_esi_scopes())
            .require_valid()
            .first()
        )
        if not token:
            raise TokenError(
                f"Token does not exist for {self} with scopes {self.get_esi_scopes()}"
            )
        return token

    @cached_property
    def character_ownership(self):
        """Return the character ownership of this character, None for orphans."""
        try:
            return self.character.character_ownership
        except ObjectDoesNotExist:
            return None

    @cached_property
    def is_orphan(self) -> bool:
        """An orphan is a character that is not owned anymore by a user."""
        return self.character_ownership is None

    # Task Area: one `update_<section>` method per CharacterUpdateSection
    def update_wallet(self, force_refresh: bool = False) -> UpdateSectionResult:
        """Update the wallet balance for this character."""
        return CharacterOwner.objects.update_wallet_esi(
            self, force_refresh=force_refresh
        )


class CharacterUpdateStatus(UpdateStatusBaseModel):
    """The update status of one section of a CharacterOwner."""

    class Meta(UpdateStatusBaseModel.Meta):
        default_permissions = ()

    objects: CharacterUpdateStatusManager = CharacterUpdateStatusManager()

    owner = models.ForeignKey(
        CharacterOwner,
        on_delete=models.CASCADE,
        related_name="example_update_status",
    )
    section = models.CharField(
        max_length=32, choices=CharacterUpdateSection.choices, db_index=True
    )


CharacterOwner.update_status_model = CharacterUpdateStatus
