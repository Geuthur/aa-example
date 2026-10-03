# Standard Library
from http import HTTPStatus

# Third Party
from ninja import NinjaAPI

# Django
from django.utils.translation import gettext as _

# AA Example
# AA Belt Radar
from example import __title__
from example.api import schema
from example.helpers.eveonline import get_character_portrait_url
from example.models.general import UserSettings


class ApiEndpoints:
    tags = ["General"]

    def __init__(self, api: NinjaAPI):
        @api.get(
            "menu/",
            response={
                HTTPStatus.OK: schema.MenuSchema,
            },
            tags=self.tags,
            summary="Get Killstats navigation menu",
        )
        def get_menu(request):  # pylint: disable=unused-argument
            left_menu: list[schema.MenuLink] = []
            left_menu.append(schema.MenuLink(name=__title__, link="/"))
            left_menu.append(schema.MenuLink(name=_("Settings"), link="/settings/"))

            right_menu: list[schema.MenuLink] = []
            return schema.MenuSchema(
                left_links=left_menu,
                right_links=right_menu,
            )

        @api.get(
            "user/",
            response={
                HTTPStatus.OK: schema.UserData,
                HTTPStatus.FORBIDDEN: dict,
            },
            tags=self.tags,
        )
        def get_user(request):
            if not request.user.has_perm("example.basic_access"):
                return HTTPStatus.FORBIDDEN, {"error": _("Permission Denied.")}

            try:
                character_id = request.user.profile.main_character.character_id
                character_name = request.user.profile.main_character.character_name
                corporation_id = request.user.profile.main_character.corporation_id
                corporation_name = request.user.profile.main_character.corporation_name
                alliance_id = request.user.profile.main_character.alliance_id
                alliance_name = request.user.profile.main_character.alliance_name
            except AttributeError:
                character_id = 0
                character_name = ""
                corporation_id = 0
                corporation_name = ""
                alliance_id = None
                alliance_name = None

            portrait_url = (
                get_character_portrait_url(
                    character_id=character_id,
                    character_name=character_name,
                    as_html=False,
                )
                if character_id
                else None
            )

            is_admin = bool(request.user.has_perm("example.full_access"))

            return HTTPStatus.OK, schema.UserData(
                user_id=request.user.id,
                character_id=character_id,
                character_name=character_name,
                corporation_id=corporation_id,
                corporation_name=corporation_name,
                alliance_id=alliance_id,
                alliance_name=alliance_name,
                portrait=portrait_url,
                is_admin=is_admin,
            )

        @api.get(
            "settings/",
            response={
                HTTPStatus.OK: schema.UserSettingsSchema,
                HTTPStatus.FORBIDDEN: dict,
            },
            tags=self.tags,
            summary="Get current user's settings",
        )
        def get_user_settings(request):
            if not request.user.has_perm("example.basic_access"):
                return HTTPStatus.FORBIDDEN, {"error": _("Permission Denied.")}

            settings = UserSettings.objects.get_or_create(user=request.user)[0]
            return schema.UserSettingsSchema(
                disable_notifications=settings.disable_notifications
            )

        @api.put(
            "settings/",
            response={
                HTTPStatus.OK: schema.UserSettingsSchema,
                HTTPStatus.FORBIDDEN: dict,
            },
            tags=self.tags,
            summary="Update current user's settings",
        )
        def update_user_settings(request, payload: schema.UserSettingsUpdateRequest):
            if not request.user.has_perm("example.basic_access"):
                return HTTPStatus.FORBIDDEN, {"error": _("Permission Denied.")}

            settings = UserSettings.objects.get_or_create(user=request.user)[0]
            settings.disable_notifications = payload.disable_notifications
            settings.save(update_fields=["disable_notifications"])
            return schema.UserSettingsSchema(
                disable_notifications=settings.disable_notifications
            )
