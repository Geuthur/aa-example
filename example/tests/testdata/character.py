"""Factories of the character module."""

# Third Party
import factory
import factory.fuzzy

# AA EVE SDE Factory
from evesde_factory.allianceauth import BaseMetaFactory

# Django
from django.utils import timezone

# AA Example
from example.models.character import CharacterOwner, CharacterUpdateStatus
from example.models.helpers.update_manager import CharacterUpdateSection
from example.tests.testdata.app import UserMainFactory


class CharacterOwnerFactory(
    factory.django.DjangoModelFactory, metaclass=BaseMetaFactory[CharacterOwner]
):
    """
    Generate a CharacterOwner object.

    Args:
        user (User, optional): The user whose main character becomes the owner. Created if not given.
        character (EveCharacter, optional): The character of the owner, defaults to the user's main character.
    """

    class Meta:
        model = CharacterOwner
        exclude = ("user",)

    user = factory.SubFactory(UserMainFactory)
    character = factory.LazyAttribute(lambda o: o.user.profile.main_character)
    active = True
    wallet_balance = None


class CharacterUpdateStatusFactory(
    factory.django.DjangoModelFactory,
    metaclass=BaseMetaFactory[CharacterUpdateStatus],
):
    """Generate a CharacterUpdateStatus object for testing."""

    class Meta:
        model = CharacterUpdateStatus
        django_get_or_create = ("owner", "section")

    owner = factory.SubFactory(CharacterOwnerFactory)
    section = factory.fuzzy.FuzzyChoice(CharacterUpdateSection.values)
    is_success = True
    error_message = ""
    has_token_error = False
    last_run_at = factory.fuzzy.FuzzyDateTime(
        start_dt=timezone.make_aware(timezone.datetime(2020, 1, 1)),
        end_dt=timezone.make_aware(timezone.datetime(2024, 12, 31)),
    )
    last_run_finished_at = factory.fuzzy.FuzzyDateTime(
        start_dt=timezone.make_aware(timezone.datetime(2020, 1, 1)),
        end_dt=timezone.make_aware(timezone.datetime(2024, 12, 31)),
    )
    last_update_at = factory.fuzzy.FuzzyDateTime(
        start_dt=timezone.make_aware(timezone.datetime(2020, 1, 1)),
        end_dt=timezone.make_aware(timezone.datetime(2024, 12, 31)),
    )
    last_update_finished_at = factory.fuzzy.FuzzyDateTime(
        start_dt=timezone.make_aware(timezone.datetime(2020, 1, 1)),
        end_dt=timezone.make_aware(timezone.datetime(2024, 12, 31)),
    )
