"""Tests that the whole API requires a login and `basic_access`."""

# Standard Library
import re
from http import HTTPStatus

# Third Party
from ninja.testing import TestClient

# Django
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

# AA Example
from example import __app_name__
from example.api import api
from example.api.auth import BasicAccessAuth
from example.models.general import General
from example.tests import AuthTestCase
from example.tests.testdata.app import UserMainFactory

BASIC_ACCESS = f"{__app_name__}.basic_access"
HIGHER_PERMISSIONS = [
    f"{__app_name__}.{codename}"
    for codename, _ in General._meta.permissions
    if codename != "basic_access"
]


def _operations():
    """Return (method, path, operation) of every operation registered in the API."""
    found = []
    for prefix, router in api._routers:  # pylint: disable=protected-access
        for path, path_view in router.path_operations.items():
            for operation in path_view.operations:
                for method in operation.methods:
                    found.append((method, f"{prefix}{path}".lstrip("/"), operation))
    return found


def _url(path: str) -> str:
    """URL of a route, every path parameter replaced by `1`."""
    return reverse(f"{__app_name__}:index") + "api/" + re.sub(r"\{[^}]+\}", "1", path)


class TestApiAuth(AuthTestCase):
    """
    Basic access is only granted by `basic_access`.

    Higher permissions do not include it: without `basic_access` every
    endpoint answers 403. The tests walk all registered routes, so a new
    endpoint is covered without any change here.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.users_without_basic_access = {
            "no permission": UserMainFactory(permissions__=[]),
            "all higher permissions": UserMainFactory(permissions__=HIGHER_PERMISSIONS),
        }
        for permission in HIGHER_PERMISSIONS:
            cls.users_without_basic_access[permission] = UserMainFactory(
                permissions__=[permission]
            )

    def _request(self, method: str, path: str):
        return self.client.generic(method, _url(path), content_type="application/json")

    def test_api_should_have_routes_and_higher_permissions(self):
        # Expected Result: the tests below must not pass on empty lists
        self.assertTrue(_operations())
        self.assertTrue(HIGHER_PERMISSIONS)
        for name, user in self.users_without_basic_access.items():
            with self.subTest(user=name):
                self.assertFalse(user.has_perm(BASIC_ACCESS))
        user = self.users_without_basic_access["all higher permissions"]
        for permission in HIGHER_PERMISSIONS:
            with self.subTest(permission=permission):
                self.assertTrue(user.has_perm(permission))

    def test_every_endpoint_should_redirect_to_login_without_login(self):
        # Alliance Auth wraps every hooked URL in `main_character_required`,
        # so a request without login never reaches the API.
        for method, path, _ in _operations():
            with self.subTest(method=method, path=path):
                # Test Action
                response = self._request(method, path)

                # Expected Result
                self.assertEqual(response.status_code, HTTPStatus.FOUND)
                self.assertIn("/account/login/", response["Location"])

    def test_every_endpoint_should_return_401_without_login(self):
        # Test Data: the API itself, without the wrapper of Alliance Auth
        client = TestClient(api)

        for method, path, _ in _operations():
            with self.subTest(method=method, path=path):
                # Test Action
                response = client.request(
                    method, "/" + re.sub(r"\{[^}]+\}", "1", path), user=AnonymousUser()
                )

                # Expected Result
                self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
                self.assertEqual(response.json(), {"detail": "Unauthorized"})

    def test_every_endpoint_should_return_403_without_basic_access(self):
        for name, user in self.users_without_basic_access.items():
            self.client.force_login(user)
            for method, path, _ in _operations():
                with self.subTest(user=name, method=method, path=path):
                    # Test Action
                    response = self._request(method, path)

                    # Expected Result
                    self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
                    self.assertEqual(response.json(), {"detail": "Forbidden"})

    def test_every_endpoint_should_pass_authentication_with_basic_access(self):
        # Test Data: a superuser passes `has_perm` without the permission
        users = {
            "basic_access": self.user,
            "superuser": UserMainFactory(permissions__=[], is_superuser=True),
        }

        for name, user in users.items():
            self.client.force_login(user)
            for method, path, _ in _operations():
                with self.subTest(user=name, method=method, path=path):
                    # Test Action
                    response = self._request(method, path)

                    # Expected Result: the endpoint itself answers (200, 404, 422, ...)
                    self.assertNotIn(
                        response.status_code,
                        (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN),
                    )

    def test_no_endpoint_should_set_its_own_auth(self):
        # Test Data
        api_auth = api.auth

        # Expected Result
        self.assertEqual(len(api_auth), 1)
        self.assertIs(type(api_auth[0]), BasicAccessAuth)
        self.assertTrue(api_auth[0].csrf)
        for method, path, operation in _operations():
            with self.subTest(method=method, path=path):
                self.assertEqual(len(operation.auth_callbacks), 1)
                self.assertIs(operation.auth_callbacks[0], api_auth[0])

    def test_post_should_return_403_without_csrf_token(self):
        # Test Data
        client = self.client_class(enforce_csrf_checks=True)
        client.force_login(self.user)
        posts = [path for method, path, _ in _operations() if method == "POST"]

        for path in posts:
            with self.subTest(path=path):
                # Test Action
                response = client.post(_url(path), content_type="application/json")

                # Expected Result
                self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
                self.assertEqual(response.json(), {"detail": "CSRF check Failed"})
