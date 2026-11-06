# Standard Library
from decimal import Decimal
from http import HTTPStatus

# Third Party
import pook
from evesde_factory.allianceauth import EveCharacterFactory

# AA Example
from example.models.character import CharacterOwner, CharacterUpdateStatus
from example.models.helpers.update_manager import CharacterUpdateSection, UpdateStatus
from example.tests import AuthTestCase
from example.tests.testdata.app import UserMainFactory
from example.tests.testdata.character import (
    CharacterOwnerFactory,
    CharacterUpdateStatusFactory,
)

ESI_BASE_URL = "https://esi.evetech.net"


class TestCharacterOwnerEsi(AuthTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.owner = CharacterOwnerFactory(user=cls.user)

    @pook.on
    def test_update_wallet_should_store_the_balance_from_esi(self):
        # Test Data
        pook.get(
            f"{ESI_BASE_URL}/characters/{self.owner.character.character_id}/wallet",
            reply=HTTPStatus.OK,
            response_json=29500.01,
        )

        # Test Action
        result = self.owner.update_wallet()

        # Expected Result
        self.owner.refresh_from_db()
        self.assertTrue(result.is_changed)
        self.assertEqual(self.owner.wallet_balance, Decimal("29500.01"))
        self.assertEqual(result.data, Decimal("29500.01"))

    @pook.on
    def test_execute_section_should_record_the_wallet_update(self):
        # Test Data
        pook.get(
            f"{ESI_BASE_URL}/characters/{self.owner.character.character_id}/wallet",
            reply=HTTPStatus.OK,
            response_json=100.5,
        )

        # Test Action
        result = self.owner.execute_section(CharacterUpdateSection.WALLET)

        # Expected Result
        self.assertTrue(result.is_updated)
        status = CharacterUpdateStatus.objects.get(
            owner=self.owner, section=CharacterUpdateSection.WALLET
        )
        self.assertTrue(status.is_success)
        self.assertEqual(self.owner.get_status, UpdateStatus.OK)

    @pook.on
    def test_execute_section_should_record_esi_server_errors(self):
        # Test Data
        pook.get(
            f"{ESI_BASE_URL}/characters/{self.owner.character.character_id}/wallet",
            reply=HTTPStatus.BAD_GATEWAY,
            response_json={"error": "Bad Gateway"},
        )

        # Test Action
        result = self.owner.execute_section(CharacterUpdateSection.WALLET)

        # Expected Result
        self.assertFalse(result.is_updated)
        self.assertFalse(result.has_token_error)
        status = CharacterUpdateStatus.objects.get(
            owner=self.owner, section=CharacterUpdateSection.WALLET
        )
        self.assertFalse(status.is_success)
        self.assertIn("502", status.error_message)

    def test_execute_section_should_record_a_missing_token(self):
        # Test Data: a character nobody owns has no token
        orphan = CharacterOwnerFactory(character=EveCharacterFactory())

        # Test Action
        result = orphan.execute_section(CharacterUpdateSection.WALLET)

        # Expected Result
        self.assertTrue(result.has_token_error)
        self.assertEqual(orphan.get_status, UpdateStatus.TOKEN_ERROR)


class TestCharacterOwnerAccess(AuthTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.owner = CharacterOwnerFactory(user=cls.user)
        cls.other_owner = CharacterOwnerFactory()

    def test_visible_to_should_return_own_characters(self):
        # Test Action
        visible = CharacterOwner.objects.visible_to(self.user)

        # Expected Result
        self.assertQuerySetEqual(visible, [self.owner])

    def test_manage_to_should_return_own_characters(self):
        # Test Action
        manageable = CharacterOwner.objects.manage_to(self.user)

        # Expected Result
        self.assertQuerySetEqual(manageable, [self.owner])

    def test_visible_to_should_return_all_for_superuser(self):
        # Test Action
        visible = CharacterOwner.objects.visible_to(self.superuser)

        # Expected Result
        self.assertEqual(visible.count(), CharacterOwner.objects.count())

    def test_manage_to_should_return_all_for_full_access(self):
        # Test Data
        admin = UserMainFactory(
            permissions__=["example.basic_access", "example.full_access"]
        )

        # Test Action
        manageable = CharacterOwner.objects.manage_to(admin)

        # Expected Result
        self.assertEqual(manageable.count(), CharacterOwner.objects.count())

    def test_visible_to_should_return_nothing_without_main_character(self):
        # Test Data
        user = UserMainFactory()
        user.profile.main_character = None
        user.profile.save()

        # Test Action
        visible = CharacterOwner.objects.visible_to(user)

        # Expected Result
        self.assertFalse(visible.exists())

    def test_visible_eve_characters_should_return_own_characters(self):
        # Test Action
        characters = CharacterOwner.objects.visible_eve_characters(self.user)

        # Expected Result
        self.assertQuerySetEqual(characters, [self.owner.character])

    def test_disable_characters_with_no_owner_should_deactivate_orphans(self):
        # Test Data
        orphan = CharacterOwnerFactory(character=EveCharacterFactory())

        # Test Action
        count = CharacterOwner.objects.disable_characters_with_no_owner()

        # Expected Result
        orphan.refresh_from_db()
        self.owner.refresh_from_db()
        self.assertEqual(count, 1)
        self.assertFalse(orphan.active)
        self.assertTrue(self.owner.active)
        self.assertEqual(CharacterOwner.objects.disable_characters_with_no_owner(), 0)

    def test_active_should_exclude_inactive_owners(self):
        # Test Data
        inactive = CharacterOwnerFactory(active=False)

        # Test Action
        active = CharacterOwner.objects.active()

        # Expected Result
        self.assertIn(self.owner, active)
        self.assertNotIn(inactive, active)


class TestCharacterUpdateStatusManager(AuthTestCase):
    def test_get_status_should_aggregate_the_sections(self):
        # Test Data
        owner = CharacterOwnerFactory(user=self.user)
        CharacterUpdateStatusFactory(
            owner=owner, section=CharacterUpdateSection.WALLET, is_success=False
        )

        # Test Action
        status = CharacterUpdateStatus.objects.filter(owner=owner).get_status()

        # Expected Result
        self.assertEqual(status, UpdateStatus.ERROR)

    def test_get_status_should_be_incomplete_without_rows(self):
        # Test Action & Expected Result
        self.assertEqual(
            CharacterUpdateStatus.objects.none().get_status(), UpdateStatus.INCOMPLETE
        )
