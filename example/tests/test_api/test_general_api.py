# Standard Library
from http import HTTPStatus

# Django
from django.urls import reverse

# AA Example
from example.tests import AuthTestCase
from example.tests.testdata.app import UserMainFactory


class TestGeneralApi(AuthTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.api_url = reverse("example:index") + "api/"

    def test_get_user_should_return_user_data_with_basic_access(self):
        # Test Data
        self.client.force_login(self.user)

        # Test Action
        response = self.client.get(self.api_url + "user/")

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()["user_id"], self.user.id)
        self.assertFalse(response.json()["is_admin"])

    def test_get_user_should_mark_full_access_as_admin(self):
        # Test Data
        admin = UserMainFactory(
            permissions__=["example.basic_access", "example.full_access"]
        )
        self.client.force_login(admin)

        # Test Action
        response = self.client.get(self.api_url + "user/")

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.json()["is_admin"])

    def test_get_user_should_return_forbidden_without_basic_access(self):
        # Test Data
        no_access = UserMainFactory(permissions__=[])
        self.client.force_login(no_access)

        # Test Action
        response = self.client.get(self.api_url + "user/")

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
