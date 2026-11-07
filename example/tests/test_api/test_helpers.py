# Third Party
from evesde_factory.allianceauth import EveCharacterFactory

# AA Example
from example.api.helpers import character, core
from example.models.character import CharacterOwner
from example.tests import AuthTestCase
from example.tests.testdata.app import UserMainFactory
from example.tests.testdata.character import CharacterOwnerFactory


class TestCoreHelpers(AuthTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.owner = CharacterOwnerFactory(user=cls.user)
        cls.other_owner = CharacterOwnerFactory()

    def test_can_view_overview_should_follow_basic_access(self):
        # Test Data
        no_access = UserMainFactory(permissions__=[])

        # Test Action & Expected Result
        self.assertTrue(core.can_view_overview(self.user))
        self.assertFalse(core.can_view_overview(no_access))

    def test_get_object_with_access_should_return_own_object(self):
        # Test Data
        request = self.factory.get("/")
        request.user = self.user

        # Test Action
        perms, obj = core.get_object_with_access(
            request, CharacterOwner.objects, pk=self.owner.pk
        )

        # Expected Result
        self.assertTrue(perms)
        self.assertEqual(obj, self.owner)

    def test_get_object_with_access_should_deny_foreign_object(self):
        # Test Data
        request = self.factory.get("/")
        request.user = self.user

        # Test Action
        perms, obj = core.get_object_with_access(
            request, CharacterOwner.objects, manage=True, pk=self.other_owner.pk
        )

        # Expected Result
        self.assertFalse(perms)
        self.assertEqual(obj, self.other_owner)

    def test_get_object_with_access_should_return_none_for_missing_object(self):
        # Test Data
        request = self.factory.get("/")
        request.user = self.user

        # Test Action
        perms, obj = core.get_object_with_access(
            request, CharacterOwner.objects, pk=999999
        )

        # Expected Result
        self.assertFalse(perms)
        self.assertIsNone(obj)


class TestCharacterHelpers(AuthTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.owner = CharacterOwnerFactory(user=cls.user)

    def test_get_character_owner_should_find_by_character_id(self):
        # Test Data
        request = self.factory.get("/")
        request.user = self.user

        # Test Action
        perms, owner = character.get_character_owner(
            request, self.owner.character.character_id
        )

        # Expected Result
        self.assertTrue(perms)
        self.assertEqual(owner, self.owner)

    def test_get_character_owner_should_allow_full_access_to_manage(self):
        # Test Data
        admin = UserMainFactory(
            permissions__=["example.basic_access", "example.full_access"]
        )
        request = self.factory.get("/")
        request.user = admin

        # Test Action
        perms, owner = character.get_character_owner(
            request, self.owner.character.character_id, manage=True
        )

        # Expected Result
        self.assertTrue(perms)
        self.assertEqual(owner, self.owner)

    def test_get_character_owner_should_return_none_for_unknown_character(self):
        # Test Data
        request = self.factory.get("/")
        request.user = self.user
        unknown = EveCharacterFactory()

        # Test Action
        perms, owner = character.get_character_owner(request, unknown.character_id)

        # Expected Result
        self.assertFalse(perms)
        self.assertIsNone(owner)
