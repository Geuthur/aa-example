"""Character API endpoints: the example module of the template."""

# Standard Library
from http import HTTPStatus

# Third Party
from ninja import NinjaAPI

# Django
from django.core.handlers.wsgi import WSGIRequest
from django.utils.translation import gettext as _

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Example
from example import __title__, tasks
from example.api import schema
from example.api.helpers.character import get_character_owner
from example.api.helpers.core import can_view_overview
from example.helpers.eveonline import get_character_portrait_url
from example.models.character import CharacterOwner
from example.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


def _serialize_character(owner: CharacterOwner) -> schema.CharacterSchema:
    """Serialize one owner for the character list."""
    status = owner.get_status
    last_update = (
        owner.example_update_status.exclude(last_update_finished_at__isnull=True)
        .order_by("-last_update_finished_at")
        .values_list("last_update_finished_at", flat=True)
        .first()
    )
    return schema.CharacterSchema(
        id=owner.pk,
        character_id=owner.character.character_id,
        character_name=owner.character.character_name,
        corporation_id=owner.character.corporation_id,
        corporation_name=owner.character.corporation_name,
        portrait_url=get_character_portrait_url(owner.character.character_id, size=64),
        active=owner.active,
        wallet_balance=(
            float(owner.wallet_balance) if owner.wallet_balance is not None else None
        ),
        update_status=status.value,
        update_status_label=str(status.label),
        last_update=last_update,
    )


def _serialize_character_detail(owner: CharacterOwner) -> schema.CharacterDetailSchema:
    """Serialize one owner with the status of every section."""
    summary = _serialize_character(owner)
    sections = [
        schema.CharacterUpdateStatusSchema(
            section=status.section,
            section_label=str(
                CharacterOwner.update_section_class(status.section).label
            ),
            is_success=status.is_success,
            has_token_error=status.has_token_error,
            error_message=status.error_message,
            last_run_finished_at=status.last_run_finished_at,
            last_update_finished_at=status.last_update_finished_at,
        )
        for status in owner.example_update_status.order_by("section")
    ]
    return schema.CharacterDetailSchema(**summary.dict(), sections=sections)


class ApiEndpoints:
    tags = ["Characters"]

    def __init__(self, api: NinjaAPI):
        @api.get(
            "characters/",
            response={
                HTTPStatus.OK: list[schema.CharacterSchema],
                HTTPStatus.FORBIDDEN: schema.ErrorSchema,
            },
            tags=self.tags,
            summary="List the characters visible to the user",
        )
        def list_characters(request: WSGIRequest):
            if not can_view_overview(request.user):
                return HTTPStatus.FORBIDDEN, {"error": _("Permission Denied")}

            owners = (
                CharacterOwner.objects.visible_to(request.user)
                .select_related("character")
                .order_by("character__character_name")
            )
            return HTTPStatus.OK, [_serialize_character(owner) for owner in owners]

        @api.get(
            "characters/{character_id}/",
            response={
                HTTPStatus.OK: schema.CharacterDetailSchema,
                HTTPStatus.FORBIDDEN: schema.ErrorSchema,
                HTTPStatus.NOT_FOUND: schema.ErrorSchema,
            },
            tags=self.tags,
            summary="Get a character with the status of its sections",
        )
        def get_character(request: WSGIRequest, character_id: int):
            perms, owner = get_character_owner(request, character_id)

            if owner is None:
                return HTTPStatus.NOT_FOUND, {"error": _("Character not found")}

            if perms is False:
                return HTTPStatus.FORBIDDEN, {"error": _("Permission Denied")}

            return HTTPStatus.OK, _serialize_character_detail(owner)

        @api.post(
            "characters/{character_id}/update/",
            response={
                HTTPStatus.OK: schema.ActionResponse,
                HTTPStatus.FORBIDDEN: schema.ErrorSchema,
                HTTPStatus.NOT_FOUND: schema.ErrorSchema,
            },
            tags=self.tags,
            summary="Queue an update of a character",
        )
        def update_character(
            request: WSGIRequest,
            character_id: int,
            payload: schema.ForceRefreshRequest | None = None,
        ):
            perms, owner = get_character_owner(request, character_id, manage=True)

            if owner is None:
                return HTTPStatus.NOT_FOUND, {"error": _("Character not found")}

            if perms is False:
                return HTTPStatus.FORBIDDEN, {"error": _("Permission Denied")}

            force_refresh = payload.force_refresh if payload else False
            tasks.update_character.apply_async(
                args=[owner.pk],
                kwargs={"force_refresh": force_refresh},
                priority=7,
            )
            logger.info("User %s queued an update for %s", request.user, owner)

            return HTTPStatus.OK, schema.ActionResponse(
                success=True,
                message=_("Update task queued for %s") % owner.character.character_name,
            )
