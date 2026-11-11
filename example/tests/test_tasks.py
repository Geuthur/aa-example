# Standard Library
from http import HTTPStatus
from unittest.mock import MagicMock, patch

# Third Party
import pook
from aiopenapi3 import RequestError
from celery.exceptions import Retry
from evesde_factory.allianceauth import EveCharacterFactory

# Django
from django.core.cache import cache
from django.test import override_settings
from django.utils import timezone

# Alliance Auth
from esi.exceptions import (
    ESIBucketLimitException,
    ESIErrorLimitException,
    HTTPServerError,
)

# AA Example
from example import tasks
from example.errors import DownTimeError
from example.models.character import CharacterUpdateStatus
from example.models.helpers.update_manager import (
    CharacterUpdateSection,
    UpdateSectionResult,
    UpdateStatus,
)
from example.providers import DOWNTIME_TIMER
from example.tests import AuthTestCase
from example.tests.testdata.character import (
    CharacterOwnerFactory,
    CharacterUpdateStatusFactory,
)
from example.tests.testdata.esi import clear_esi_limits, wallet_url

TASK_PATH = "example.tasks"


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
@patch(TASK_PATH + ".update_character", spec=True)
class TestUpdateAllCharacters(AuthTestCase):
    def test_should_queue_active_characters_only(self, mock_update_character):
        # Test Data
        owner = CharacterOwnerFactory(user=self.user)
        CharacterOwnerFactory(active=False)

        # Test Action
        count = tasks.update_all_characters()

        # Expected Result
        self.assertEqual(count, 1)
        mock_update_character.apply_async.assert_called_once_with(
            args=[owner.pk], kwargs={"force_refresh": False}
        )

    def test_should_disable_orphans_before_queueing(self, mock_update_character):
        # Test Data
        orphan = CharacterOwnerFactory(character=EveCharacterFactory())

        # Test Action
        count = tasks.update_all_characters(force_refresh=True)

        # Expected Result
        orphan.refresh_from_db()
        self.assertFalse(orphan.active)
        self.assertEqual(count, 0)
        mock_update_character.apply_async.assert_not_called()


@override_settings(
    CELERY_ALWAYS_EAGER=True,
    CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
    DISABLE_DAILY_DOWNTIME_CHECK=True,
)
class TestUpdateCharacter(AuthTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.owner = CharacterOwnerFactory(user=cls.user)

    @patch(TASK_PATH + ".CharacterOwner.execute_section", autospec=True)
    def test_should_execute_stale_sections(self, mock_execute_section):
        # Test Data
        mock_execute_section.return_value = UpdateSectionResult(
            is_changed=True, is_updated=True
        )

        # Test Action
        result = tasks.update_character(self.owner.pk)

        # Expected Result
        self.assertTrue(result)
        mock_execute_section.assert_called_once_with(
            self.owner, CharacterUpdateSection.WALLET.value, force_refresh=False
        )

    @patch(TASK_PATH + ".CharacterOwner.execute_section", autospec=True)
    def test_should_skip_fresh_sections(self, mock_execute_section):
        # Test Data
        CharacterUpdateStatusFactory(
            owner=self.owner,
            section=CharacterUpdateSection.WALLET,
            last_run_finished_at=timezone.now(),
        )

        # Test Action
        result = tasks.update_character(self.owner.pk)

        # Expected Result
        self.assertFalse(result)
        mock_execute_section.assert_not_called()

    @patch(TASK_PATH + ".CharacterOwner.execute_section", autospec=True)
    def test_should_force_refresh_every_section(self, mock_execute_section):
        # Test Data
        CharacterUpdateStatusFactory(
            owner=self.owner,
            section=CharacterUpdateSection.WALLET,
            last_run_finished_at=timezone.now(),
        )

        # Test Action
        result = tasks.update_character(self.owner.pk, force_refresh=True)

        # Expected Result
        self.assertTrue(result)
        mock_execute_section.assert_called_once_with(
            self.owner, CharacterUpdateSection.WALLET.value, force_refresh=True
        )

    @patch(TASK_PATH + ".CharacterOwner.execute_section", autospec=True)
    def test_should_skip_orphans(self, mock_execute_section):
        # Test Data
        orphan = CharacterOwnerFactory(character=EveCharacterFactory())

        # Test Action
        result = tasks.update_character(orphan.pk)

        # Expected Result
        self.assertFalse(result)
        mock_execute_section.assert_not_called()

    def test_should_return_false_for_unknown_owner(self):
        # Test Action & Expected Result
        self.assertFalse(tasks.update_character(999999))

    @patch(TASK_PATH + ".retry_task_on_esi_error")
    def test_should_run_the_sections_inside_the_retry_context(self, mock_retry):
        # Test Data
        mock_retry.return_value.__enter__ = MagicMock()
        mock_retry.return_value.__exit__ = MagicMock(return_value=False)

        # Test Action
        with patch(TASK_PATH + ".CharacterOwner.execute_section", autospec=True):
            tasks.update_character(self.owner.pk)

        # Expected Result
        mock_retry.assert_called_once()
        mock_retry.return_value.__enter__.assert_called_once()

    @override_settings(DISABLE_DAILY_DOWNTIME_CHECK=False)
    @patch(TASK_PATH + ".CharacterOwner.execute_section", autospec=True)
    def test_should_retry_during_daily_downtime(self, mock_execute_section):
        # Test Data
        with patch("example.providers.timezone.now") as mock_now:
            mock_now.return_value = timezone.datetime.strptime("11:05", "%H:%M")

            # Test Action & Expected Result: the retry raises in eager mode
            with self.assertRaises(DownTimeError):
                tasks.update_character(self.owner.pk)
        mock_execute_section.assert_not_called()


@override_settings(
    CELERY_ALWAYS_EAGER=True,
    CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
    DISABLE_DAILY_DOWNTIME_CHECK=True,
)
@patch.object(tasks.update_character, "retry", side_effect=Retry)
class TestUpdateCharacterEsiErrors(AuthTestCase):
    """ESI errors of a section reach `retry_task_on_esi_error` through the UpdateManager."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.owner = CharacterOwnerFactory(user=cls.user)

    def setUp(self):
        super().setUp()
        clear_esi_limits(self.owner)
        self.addCleanup(clear_esi_limits, self.owner)

    def _assert_retried(self, mock_retry, exc_type, countdown_min: float):
        mock_retry.assert_called_once()
        kwargs = mock_retry.call_args.kwargs
        self.assertIsInstance(kwargs["exc"], exc_type)
        self.assertGreaterEqual(kwargs["countdown"], countdown_min)
        status = CharacterUpdateStatus.objects.get(
            owner=self.owner, section=CharacterUpdateSection.WALLET
        )
        self.assertFalse(status.is_success)
        self.assertTrue(status.error_message.startswith(exc_type.__name__))

    def test_should_retry_on_esi_server_errors(self, mock_retry):
        for status_code in [
            HTTPStatus.BAD_GATEWAY,
            HTTPStatus.SERVICE_UNAVAILABLE,
            HTTPStatus.GATEWAY_TIMEOUT,
        ]:
            with self.subTest(status_code=status_code), pook.use():
                # Test Data
                mock_retry.reset_mock()
                pook.get(
                    wallet_url(self.owner),
                    reply=status_code,
                    response_json={"error": status_code.phrase},
                )

                # Test Action
                with self.assertRaises(Retry):
                    tasks.update_character(self.owner.pk)

                # Expected Result
                self._assert_retried(mock_retry, HTTPServerError, DOWNTIME_TIMER)

    @pook.on
    def test_should_retry_on_the_esi_error_limit(self, mock_retry):
        # Test Data
        pook.get(
            wallet_url(self.owner),
            reply=420,
            response_json={"error": "Error limited"},
            response_headers={"X-RateLimit-Reset": "30"},
        )

        # Test Action
        with self.assertRaises(Retry):
            tasks.update_character(self.owner.pk)

        # Expected Result
        self._assert_retried(mock_retry, ESIErrorLimitException, 30)

    @pook.on
    def test_should_retry_on_the_esi_bucket_limit(self, mock_retry):
        # Test Data: the wallet bucket of the character is used up
        cache.set(
            f"esi:bucket:char-wallet:{self.owner.character.character_id}",
            0,
            timeout=900,
        )

        # Test Action
        with self.assertRaises(Retry):
            tasks.update_character(self.owner.pk)

        # Expected Result
        self._assert_retried(mock_retry, ESIBucketLimitException, 1)

    @pook.on
    @patch("esi.app_settings.ESI_SERVER_ERROR_MAX_RETRIES", 1)
    def test_should_retry_on_request_errors(self, mock_retry):
        # Test Data
        pook.get(wallet_url(self.owner)).error(ConnectionError("Connection reset"))

        # Test Action
        with self.assertRaises(Retry):
            tasks.update_character(self.owner.pk)

        # Expected Result
        self._assert_retried(mock_retry, RequestError, DOWNTIME_TIMER)

    @patch(TASK_PATH + ".CharacterOwner.update_wallet", autospec=True)
    def test_should_retry_on_downtime_errors_of_a_section(
        self, mock_update_wallet, mock_retry
    ):
        # Test Data
        mock_update_wallet.side_effect = DownTimeError("ESI is in daily downtime")

        # Test Action
        with self.assertRaises(Retry):
            tasks.update_character(self.owner.pk)

        # Expected Result
        self._assert_retried(mock_retry, DownTimeError, DOWNTIME_TIMER)

    def test_should_record_other_esi_errors_without_retry(self, mock_retry):
        for status_code in [HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.NOT_FOUND]:
            with self.subTest(status_code=status_code), pook.use():
                # Test Data
                pook.get(
                    wallet_url(self.owner),
                    reply=status_code,
                    response_json={"error": status_code.phrase},
                )

                # Test Action
                result = tasks.update_character(self.owner.pk)

                # Expected Result
                self.assertTrue(result)
                mock_retry.assert_not_called()
                status = CharacterUpdateStatus.objects.get(
                    owner=self.owner, section=CharacterUpdateSection.WALLET
                )
                self.assertFalse(status.is_success)
                self.assertIn(str(status_code.value), status.error_message)
                self.assertEqual(self.owner.get_status, UpdateStatus.ERROR)
