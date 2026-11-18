"""Authentication of the API: a logged in user with `basic_access`."""

# Third Party
from ninja.errors import AuthorizationError
from ninja.security import SessionAuth

# AA Example
from example.managers.general import GeneralManager


class BasicAccessAuth(SessionAuth):
    """
    Session authentication that also requires `basic_access`.

    Basic access is only granted by `basic_access`; higher permissions do not
    include it. The API is created with this class, so every endpoint answers
    401 without a login and 403 without `basic_access` before its own code
    runs. No endpoint or router sets its own `auth`.
    """

    def authenticate(self, request, key):
        user = super().authenticate(request, key)
        if user is None:
            return None
        if not GeneralManager.has_basic_access(user):
            raise AuthorizationError()
        return user
