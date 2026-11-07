# Standard Library
from unittest.mock import MagicMock, patch

# Third Party
from evesde_factory.allianceauth import EveCharacterFactory

# Django
from django.test import override_settings
from django.utils import timezone

# AA Example
from example import tasks
from example.errors import DownTimeError
from example.models.helpers.update_manager import (
    CharacterUpdateSection,
    UpdateSectionResult,
)
from example.tests import AuthTestCase
from example.tests.testdata.character import (
    CharacterOwnerFactory,
    CharacterUpdateStatusFactory,
)

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


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
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
