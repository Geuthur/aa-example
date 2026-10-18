"""Template for a TestView class."""

# Standard Library
from http import HTTPStatus

# Django
from django.urls import reverse

# AA Example
from example import views
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

    def test_react_base_with_character_id_should_render_view(self):
        # Test Data
        character_id = 987654321
        request = self.factory.get(
            reverse("example:react_base", kwargs={"character_id": character_id})
        )
        request.user = self.user

        # Test Action
        response = views.react_base(request, character_id=character_id)

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "aa-example-root")
