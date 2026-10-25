"""Hook into Alliance Auth"""

# Django
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

# AA Example
from example import app_settings, urls
from example.models.general import General


class ExampleMenuItem(MenuItemHook):
    """This class ensures only authorized users will see the menu entry"""

    def __init__(self):
        super().__init__(
            f"{app_settings.EXAMPLE_APP_NAME}",
            "fas fa-book fa-fw",
            "example:index",
            navactive=["example:"],
        )

    def render(self, request):
        if General.has_perm(request.user, General.Permission.BASIC_ACCESS):
            return MenuItemHook.render(self, request)
        return ""


@hooks.register("menu_item_hook")
def register_menu():
    """Register the menu item"""

    return ExampleMenuItem()


@hooks.register("url_hook")
def register_urls():
    """Register app urls"""

    return UrlHook(urls, "example", r"^example/")
