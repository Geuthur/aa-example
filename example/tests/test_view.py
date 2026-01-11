"""Template for a TestView class."""

# Standard Library
from http import HTTPStatus

# Django
from django.test import RequestFactory, TestCase
from django.urls import reverse

# AA Example
from example.tests.testdata.utils import create_user_from_evecharacter
from example.views import index


class TestViews(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = RequestFactory()
        cls.user = create_user_from_evecharacter(
            permissions=[
                "example.basic_access",
            ]
        )

    def test_view(self):
        request = self.factory.get(reverse("example:index"))
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)
