"""Template for a TestView class."""

# Standard Library
from http import HTTPStatus

# Django
from django.urls import reverse

# AA Example
from example import views
from example.models.general import General
from example.tests import AuthTestCase


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


class TestGeneralPermissions(AuthTestCase):
    def test_get_perm_should_prefix_codename_with_app_label(self):
        # Test Data
        perm = General.Permission.BASIC_ACCESS

        # Test Action
        result = General.get_perm(perm)

        # Expected Result
        self.assertEqual(result, "example.basic_access")

    def test_has_perm_should_return_false_for_missing_user(self):
        # Test Data
        user = None

        # Test Action
        result = General.has_perm(user, General.Permission.BASIC_ACCESS)

        # Expected Result
        self.assertFalse(result)

    def test_has_management_access_should_return_false_without_permission(self):
        # Test Data
        user = self.user

        # Test Action
        result = General.has_management_access(user)

        # Expected Result
        self.assertFalse(result)
