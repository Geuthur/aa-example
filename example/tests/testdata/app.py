# Third Party
import factory

# AA EVE SDE Factory
from evesde_factory.allianceauth import UserFactory

# Django
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Alliance Auth
from allianceauth.tests.auth_utils import AuthUtils

# AA Example
from example import __app_name__
from example.tests.testdata.factory import EveCharacterFactory
from example.tests.testdata.utils import add_character_to_user


class UserMainFactory(UserFactory):
    """Generate a User object with a main character and default permissions for Alliance Auth."""

    permissions__ = [f"{__app_name__}.basic_access"]
    scopes__ = ["publicData"]

    # pylint: disable=no-self-argument
    @factory.post_generation
    def permissions(obj, create, extracted, **kwargs):
        """Set permissions. Overwrite with `permissions=["app.perm1"]`."""
        if not create:
            return
        for permission_name in extracted or []:
            # The template models are abstract, so their permissions are never
            # created by migrations. Create them on demand for the tests only.
            app_label, codename = permission_name.split(".")
            content_type, _ = ContentType.objects.get_or_create(
                app_label=app_label, model="general"
            )
            Permission.objects.get_or_create(
                content_type=content_type,
                codename=codename,
                defaults={"name": codename},
            )
            AuthUtils.add_permission_to_user_by_name(permission_name, obj)

    @factory.post_generation
    def main_character(obj, create, _, **kwargs):
        if not create:
            return
        if "character" in kwargs:
            character = kwargs["character"]
        else:
            character_name = f"{obj.first_name} {obj.last_name}"
            character = EveCharacterFactory(character_name=character_name)

        add_character_to_user(
            user=obj,
            character=character,
            is_main=True,
            scopes=obj._main_character_scopes,
        )
