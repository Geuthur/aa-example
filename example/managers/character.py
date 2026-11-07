"""Managers of the character module: owner access, ESI fetch and update status."""

# Standard Library
from decimal import Decimal
from typing import TYPE_CHECKING

# Django
from django.db import models
from django.db.models import Case, Count, Q, Value, When

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Example
from example import __title__
from example.managers.general import AccessManager, AccessQuerySet
from example.models.helpers.update_manager import (
    CharacterUpdateSection,
    UpdateSectionResult,
    UpdateStatus,
)
from example.providers import AppLogger, esi

if TYPE_CHECKING:
    # AA Example
    from example.models.character import CharacterOwner, CharacterUpdateStatus

logger = AppLogger(my_logger=get_extension_logger(__name__), prefix=__title__)


class CharacterOwnerQuerySet(AccessQuerySet["CharacterOwner"]):
    def active(self):
        """Return owners that are updated."""
        return self.filter(active=True)

    def disable_characters_with_no_owner(self) -> int:
        """Disable characters which have no owner. Return count of disabled characters."""
        orphaned_characters = self.filter(
            character__character_ownership__isnull=True, active=True
        )
        if orphaned_characters.exists():
            orphans = list(
                orphaned_characters.values_list(
                    "character__character_name", flat=True
                ).order_by("character__character_name")
            )
            orphaned_characters.update(active=False)
            logger.info(
                "Disabled %d characters which do not belong to a user: %s",
                len(orphans),
                ", ".join(orphans),
            )
            return len(orphans)
        return 0


class CharacterOwnerManager(AccessManager["CharacterOwner"]):
    def get_queryset(self):
        return CharacterOwnerQuerySet(self.model, using=self._db)

    def active(self):
        """Return owners that are updated."""
        return self.get_queryset().active()

    def disable_characters_with_no_owner(self) -> int:
        """Disable characters which have no owner. Return count of disabled characters."""
        return self.get_queryset().disable_characters_with_no_owner()

    # ESI section: the owner's `update_<section>` method calls this
    def update_wallet_esi(
        self, owner: "CharacterOwner", force_refresh: bool = False
    ) -> UpdateSectionResult:
        """Update the wallet balance of an owner from ESI."""
        return owner.update_manager.update_section_if_changed(
            section=CharacterUpdateSection.WALLET,
            fetch_func=self._fetch_wallet_esi,
            force_refresh=force_refresh,
        )

    def _fetch_wallet_esi(
        self, owner: "CharacterOwner", force_refresh: bool = False
    ) -> Decimal:
        """Fetch the wallet balance from ESI and store it on the owner."""
        token = owner.get_token()

        wallet = esi.client.Wallet.GetCharactersCharacterIdWallet(
            character_id=owner.character.character_id,
            token=token,
        )
        balance = wallet.result(force_refresh=force_refresh)

        owner.wallet_balance = Decimal(str(balance))
        owner.save(update_fields=["wallet_balance"])
        return owner.wallet_balance


class CharacterUpdateStatusQuerySet(models.QuerySet["CharacterUpdateStatus"]):
    def get_status(self) -> UpdateStatus:
        """Return the current aggregate update status."""
        total_update_status = (
            self.annotate_total_update_status()
            .values_list("total_update_status", flat=True)
            .order_by("total_update_status")
            .first()
        )

        if total_update_status is None:
            return UpdateStatus.INCOMPLETE
        return UpdateStatus(total_update_status)

    def annotate_total_update_status(self):
        """Annotate one aggregate status per owner over all sections."""
        sections = CharacterUpdateSection.get_sections()
        total_sections = len(sections)
        qs = (
            self.values("owner_id", "owner__active")
            .annotate(num_sections_found=Count("pk", filter=Q(section__in=sections)))
            .annotate(
                num_sections_ok=Count(
                    "pk", filter=Q(section__in=sections, is_success=True)
                )
            )
            .annotate(
                num_sections_failed=Count(
                    "pk", filter=Q(section__in=sections, is_success=False)
                )
            )
            .annotate(
                num_sections_token_error=Count(
                    "pk", filter=Q(section__in=sections, has_token_error=True)
                )
            )
            # pylint: disable=no-member
            .annotate(
                total_update_status=Case(
                    When(owner__active=False, then=Value(UpdateStatus.DISABLED)),
                    When(
                        num_sections_token_error__gt=0,
                        then=Value(UpdateStatus.TOKEN_ERROR),
                    ),
                    When(num_sections_failed__gt=0, then=Value(UpdateStatus.ERROR)),
                    When(num_sections_ok=total_sections, then=Value(UpdateStatus.OK)),
                    When(
                        num_sections_found__lt=total_sections,
                        then=Value(UpdateStatus.INCOMPLETE),
                    ),
                    default=Value(UpdateStatus.IN_PROGRESS),
                )
            )
        )

        return qs


class CharacterUpdateStatusManager(models.Manager["CharacterUpdateStatus"]):
    def get_queryset(self):
        return CharacterUpdateStatusQuerySet(model=self.model, using=self._db)

    def get_status(self) -> UpdateStatus:
        """Return the current aggregate update status."""
        return self.get_queryset().get_status()

    def annotate_total_update_status(self):
        """Annotate one aggregate status per owner over all sections."""
        return self.get_queryset().annotate_total_update_status()
