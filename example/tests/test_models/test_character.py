# Third Party
from evesde_factory.allianceauth import EveCharacterFactory

# Alliance Auth
from esi.errors import TokenError

# AA Example
from example.models.helpers.update_manager import CharacterUpdateSection, UpdateStatus
from example.tests import AuthTestCase
from example.tests.testdata.character import (
    CharacterOwnerFactory,
    CharacterUpdateStatusFactory,
)


class TestCharacterOwner(AuthTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.owner = CharacterOwnerFactory(user=cls.user)

    def test_str_should_be_the_character_name(self):
        # Test Action & Expected Result
        self.assertEqual(str(self.owner), self.owner.character.character_name)

    def test_get_token_should_return_the_token_with_the_app_scopes(self):
        # Test Action
        token = self.owner.get_token()

        # Expected Result
        self.assertEqual(token.character_id, self.owner.character.character_id)

    def test_get_token_should_raise_without_token(self):
        # Test Data: a character nobody owns has no token
        orphan = CharacterOwnerFactory(character=EveCharacterFactory())

        # Test Action & Expected Result
        with self.assertRaises(TokenError):
            orphan.get_token()

    def test_is_orphan_should_be_false_for_owned_characters(self):
        # Test Action & Expected Result
        self.assertFalse(self.owner.is_orphan)
        self.assertEqual(self.owner.character_ownership.user, self.user)

    def test_is_orphan_should_be_true_without_ownership(self):
        # Test Data
        orphan = CharacterOwnerFactory(character=EveCharacterFactory())

        # Test Action & Expected Result
        self.assertTrue(orphan.is_orphan)

    def test_get_status_should_be_incomplete_without_status_rows(self):
        # Test Action & Expected Result
        self.assertEqual(self.owner.get_status, UpdateStatus.INCOMPLETE)

    def test_get_status_should_be_ok_when_all_sections_succeeded(self):
        # Test Data
        CharacterUpdateStatusFactory(
            owner=self.owner, section=CharacterUpdateSection.WALLET, is_success=True
        )

        # Test Action & Expected Result
        self.assertEqual(self.owner.get_status, UpdateStatus.OK)

    def test_get_status_should_be_token_error_when_a_section_has_one(self):
        # Test Data
        CharacterUpdateStatusFactory(
            owner=self.owner,
            section=CharacterUpdateSection.WALLET,
            is_success=False,
            has_token_error=True,
        )

        # Test Action & Expected Result
        self.assertEqual(self.owner.get_status, UpdateStatus.TOKEN_ERROR)

    def test_get_status_should_be_disabled_for_inactive_owners(self):
        # Test Data
        owner = CharacterOwnerFactory(active=False)

        # Test Action & Expected Result
        self.assertEqual(owner.get_status, UpdateStatus.DISABLED)

    def test_update_status_str_should_name_owner_and_section(self):
        # Test Data
        status = CharacterUpdateStatusFactory(
            owner=self.owner, section=CharacterUpdateSection.WALLET
        )

        # Test Action & Expected Result
        self.assertEqual(str(status), f"{self.owner} - wallet")
