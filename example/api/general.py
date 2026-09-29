# Standard Library
from http import HTTPStatus

# Third Party
from ninja import NinjaAPI

# Django
from django.utils.translation import gettext as _

# AA Example
# AA Belt Radar
from example import __title__, forms
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
            if not request.user.has_perm("killstats.basic_access"):
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

            settings = UserSettings.objects.get_or_create(user=request.user)[0]
            is_admin = bool(request.user.has_perm("example.admin_access"))

            return HTTPStatus.OK, schema.UserData(
                user_id=request.user.id,
                character_id=character_id,
                character_name=character_name,
                corporation_id=corporation_id,
                corporation_name=corporation_name,
                alliance_id=alliance_id,
                alliance_name=alliance_name,
                portrait=portrait_url,
                notification=settings.disable_notifications,
                is_admin=is_admin,
            )

        @api.post(
            "modify/user/settings/",
            response={
                HTTPStatus.OK: dict,
                HTTPStatus.BAD_REQUEST: dict,
                HTTPStatus.FORBIDDEN: dict,
            },
            tags=self.tags,
        )
        def modify_user_settings(request):
            if not request.user.has_perm("example.basic_access"):
                return HTTPStatus.FORBIDDEN, {"error": _("Permission Denied.")}

            settings = UserSettings.objects.get_or_create(user=request.user)[0]

            form = forms.UserSettingsForm(data=request.POST, instance=settings)
            if form.is_valid():
                form.save()
                return HTTPStatus.OK, {
                    "success": True,
                    "message": str(_("User settings updated successfully.")),
                }

            msg = _("Invalid input data. Please check the format and try again.")
            return HTTPStatus.BAD_REQUEST, {"success": False, "message": msg}
