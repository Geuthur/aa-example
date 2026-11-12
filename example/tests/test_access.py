"""Template for a TestView class."""

# Standard Library
from http import HTTPStatus

# Django
from django.urls import reverse

# AA Example
from example import views
from example.managers.general import GeneralManager
from example.tests import AuthTestCase
from example.tests.testdata.app import UserMainFactory


class TestViews(AuthTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_react_base_should_render_view(self):
        # Test Data
        request = self.factory.get(reverse("example:react_base"))
        request.user = self.user

        # Test Action
        response = views.react_base(request)

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "aa-example-root")


class TestGeneralManager(AuthTestCase):
    def test_has_management_access_should_return_false_without_permission(self):
        # Test Data
        user = self.user

        # Test Action
        result = GeneralManager.has_management_access(user)

        # Expected Result
        self.assertFalse(result)

    def test_has_management_access_should_return_true_for_manage_access(self):
        # Test Data
        user = UserMainFactory(
            permissions__=["example.basic_access", "example.manage_access"]
        )

        # Test Action
        result = GeneralManager.has_management_access(user)

        # Expected Result
        self.assertTrue(result)

    def test_has_full_access_should_return_true_only_for_full_access(self):
        # Test Data
        manager = GeneralManager
        user_manage = UserMainFactory(permissions__=["example.manage_access"])
        user_full = UserMainFactory(permissions__=["example.full_access"])

        # Expected Result
        self.assertFalse(manager.has_full_access(user_manage))
        self.assertTrue(manager.has_full_access(user_full))
