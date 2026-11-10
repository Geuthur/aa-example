# Standard Library
from decimal import Decimal
from http import HTTPStatus
from unittest.mock import patch

# Third Party
import pook
from aiopenapi3 import RequestError
from evesde_factory.allianceauth import EveCharacterFactory

# Alliance Auth
from esi.exceptions import (
    ESIBucketLimitException,
    ESIErrorLimitException,
    HTTPServerError,
)

# AA Example
from example.models.character import CharacterOwner, CharacterUpdateStatus
from example.models.helpers.update_manager import CharacterUpdateSection, UpdateStatus
from example.tests import AuthTestCase
from example.tests.testdata.app import UserMainFactory
from example.tests.testdata.character import (
    CharacterOwnerFactory,
    CharacterUpdateStatusFactory,
)
from example.tests.testdata.esi import clear_esi_limits, wallet_url


class TestCharacterOwnerEsi(AuthTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.owner = CharacterOwnerFactory(user=cls.user)

    def setUp(self):
        super().setUp()
        clear_esi_limits(self.owner)
        self.addCleanup(clear_esi_limits, self.owner)

    @pook.on
    def test_update_wallet_should_store_the_balance_from_esi(self):
        # Test Data
        pook.get(
            wallet_url(self.owner),
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
            wallet_url(self.owner),
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

    def _wallet_status(self) -> CharacterUpdateStatus:
        return CharacterUpdateStatus.objects.get(
            owner=self.owner, section=CharacterUpdateSection.WALLET
        )

    def test_execute_section_should_record_other_esi_errors(self):
        for status_code in [HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.NOT_FOUND]:
            with self.subTest(status_code=status_code), pook.use():
                # Test Data
                pook.get(
                    wallet_url(self.owner),
                    reply=status_code,
                    response_json={"error": status_code.phrase},
                )

                # Test Action
                result = self.owner.execute_section(CharacterUpdateSection.WALLET)

                # Expected Result
                self.assertFalse(result.is_updated)
                self.assertFalse(result.has_token_error)
                status = self._wallet_status()
                self.assertFalse(status.is_success)
                self.assertIn(str(status_code.value), status.error_message)
                self.assertEqual(self.owner.get_status, UpdateStatus.ERROR)

    def test_execute_section_should_raise_esi_server_errors_to_retry(self):
        for status_code in [
            HTTPStatus.BAD_GATEWAY,
            HTTPStatus.SERVICE_UNAVAILABLE,
            HTTPStatus.GATEWAY_TIMEOUT,
        ]:
            with self.subTest(status_code=status_code), pook.use():
                # Test Data
                pook.get(
                    wallet_url(self.owner),
                    reply=status_code,
                    response_json={"error": status_code.phrase},
                )

                # Test Action
                with self.assertRaises(HTTPServerError) as ctx:
                    self.owner.execute_section(CharacterUpdateSection.WALLET)

                # Expected Result
                self.assertEqual(ctx.exception.status_code, status_code)
                status = self._wallet_status()
                self.assertFalse(status.is_success)
                self.assertIn(str(status_code.value), status.error_message)

    @pook.on
    def test_execute_section_should_raise_the_esi_error_limit_to_retry(self):
        # Test Data
        pook.get(
            wallet_url(self.owner),
            reply=420,
            response_json={"error": "Error limited"},
            response_headers={"X-RateLimit-Reset": "30"},
        )

        # Test Action
        with self.assertRaises(ESIErrorLimitException) as ctx:
            self.owner.execute_section(CharacterUpdateSection.WALLET)

        # Expected Result
        self.assertEqual(ctx.exception.reset, 30)
        self.assertIn("ESIErrorLimitException", self._wallet_status().error_message)

    @pook.on
    def test_execute_section_should_raise_the_esi_bucket_limit_to_retry(self):
        # Test Data: ESI reports the wallet bucket as used up
        pook.get(
            wallet_url(self.owner),
            reply=HTTPStatus.OK,
            response_json=100.5,
            response_headers={
                "X-Ratelimit-Group": "char-wallet",
                "X-Ratelimit-Limit": "150/15m",
                "X-Ratelimit-Remaining": "0",
                "X-Ratelimit-Used": "150",
            },
        )
        self.owner.execute_section(CharacterUpdateSection.WALLET)

        # Test Action
        with self.assertRaises(ESIBucketLimitException):
            self.owner.execute_section(
                CharacterUpdateSection.WALLET, force_refresh=True
            )

        # Expected Result
        self.assertIn("ESIBucketLimitException", self._wallet_status().error_message)

    @pook.on
    @patch("esi.app_settings.ESI_SERVER_ERROR_MAX_RETRIES", 1)
    def test_execute_section_should_raise_request_errors_to_retry(self):
        # Test Data: the connection to ESI fails
        pook.get(wallet_url(self.owner)).error(ConnectionError("Connection reset"))

        # Test Action
        with self.assertRaises(RequestError):
            self.owner.execute_section(CharacterUpdateSection.WALLET)

        # Expected Result
        self.assertIn("RequestError", self._wallet_status().error_message)

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
