# Standard Library
from http import HTTPStatus
from unittest.mock import patch

# Django
from django.urls import reverse

# AA Example
from example.models.helpers.update_manager import CharacterUpdateSection
from example.tests import AuthTestCase
from example.tests.testdata.app import UserMainFactory
from example.tests.testdata.character import (
    CharacterOwnerFactory,
    CharacterUpdateStatusFactory,
)

MODULE_PATH = "example.api.character"


class TestCharacterApi(AuthTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.owner = CharacterOwnerFactory(user=cls.user, wallet_balance="1234.56")
        cls.other_owner = CharacterOwnerFactory()
        cls.api_url = reverse("example:index") + "api/"

    def test_list_characters_should_return_visible_characters(self):
        # Test Data
        CharacterUpdateStatusFactory(
            owner=self.owner, section=CharacterUpdateSection.WALLET, is_success=True
        )
        self.client.force_login(self.user)

        # Test Action
        response = self.client.get(self.api_url + "characters/")

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["character_id"], self.owner.character.character_id)
        self.assertEqual(data[0]["wallet_balance"], 1234.56)
        self.assertEqual(data[0]["update_status"], "ok")
        self.assertIn("portrait_url", data[0])

    def test_list_characters_should_return_all_for_full_access(self):
        # Test Data
        admin = UserMainFactory(
            permissions__=["example.basic_access", "example.full_access"]
        )
        self.client.force_login(admin)

        # Test Action
        response = self.client.get(self.api_url + "characters/")

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()), 2)

    def test_list_characters_should_be_forbidden_without_basic_access(self):
        # Test Data
        self.client.force_login(UserMainFactory(permissions__=[]))

        # Test Action
        response = self.client.get(self.api_url + "characters/")

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(response.json(), {"error": "Permission Denied"})

    def test_get_character_should_return_the_sections(self):
        # Test Data
        CharacterUpdateStatusFactory(
            owner=self.owner,
            section=CharacterUpdateSection.WALLET,
            is_success=False,
            error_message="HTTPServerError: 502",
        )
        self.client.force_login(self.user)

        # Test Action
        response = self.client.get(
            self.api_url + f"characters/{self.owner.character.character_id}/"
        )

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertEqual(data["update_status"], "error")
        self.assertEqual(len(data["sections"]), 1)
        self.assertEqual(data["sections"][0]["section"], "wallet")
        self.assertEqual(data["sections"][0]["section_label"], "Wallet")
        self.assertEqual(data["sections"][0]["error_message"], "HTTPServerError: 502")

    def test_get_character_should_be_forbidden_for_foreign_character(self):
        # Test Data
        self.client.force_login(self.user)

        # Test Action
        response = self.client.get(
            self.api_url + f"characters/{self.other_owner.character.character_id}/"
        )

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_get_character_should_be_not_found_for_unknown_character(self):
        # Test Data
        self.client.force_login(self.user)

        # Test Action
        response = self.client.get(self.api_url + "characters/999999999/")

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json(), {"error": "Character not found"})

    @patch(MODULE_PATH + ".tasks.update_character", spec=True)
    def test_update_character_should_queue_the_task(self, mock_task):
        # Test Data
        self.client.force_login(self.user)

        # Test Action
        response = self.client.post(
            self.api_url + f"characters/{self.owner.character.character_id}/update/",
            data={"force_refresh": True},
            content_type="application/json",
        )

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.json()["success"])
        mock_task.apply_async.assert_called_once_with(
            args=[self.owner.pk], kwargs={"force_refresh": True}, priority=7
        )

    @patch(MODULE_PATH + ".tasks.update_character", spec=True)
    def test_update_character_should_default_to_no_force_refresh(self, mock_task):
        # Test Data
        self.client.force_login(self.user)

        # Test Action
        response = self.client.post(
            self.api_url + f"characters/{self.owner.character.character_id}/update/",
            content_type="application/json",
        )

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            mock_task.apply_async.call_args.kwargs["kwargs"], {"force_refresh": False}
        )

    @patch(MODULE_PATH + ".tasks.update_character", spec=True)
    def test_update_character_should_be_forbidden_for_foreign_character(
        self, mock_task
    ):
        # Test Data
        self.client.force_login(self.user)

        # Test Action
        response = self.client.post(
            self.api_url
            + f"characters/{self.other_owner.character.character_id}/update/",
            content_type="application/json",
        )

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        mock_task.apply_async.assert_not_called()

    def test_update_character_should_be_not_found_for_unknown_character(self):
        # Test Data
        self.client.force_login(self.user)

        # Test Action
        response = self.client.post(
            self.api_url + "characters/999999999/update/",
            content_type="application/json",
        )

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestMenuApi(AuthTestCase):
    def test_menu_should_contain_the_characters_link(self):
        # Test Data
        self.client.force_login(self.user)

        # Test Action
        response = self.client.get(reverse("example:index") + "api/menu/")

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        links = {link["name"]: link["link"] for link in response.json()["left_links"]}
        self.assertEqual(links["Characters"], "/characters/")
