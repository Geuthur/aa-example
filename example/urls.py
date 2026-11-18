"""App URLs"""

# Django
from django.urls import path, re_path

# Alliance Auth
from allianceauth.authentication.decorators import decorate_url_patterns

# AA Example
from example.api import api
from example.api.auth import basic_access_required
from example.views import react_base

app_name: str = "example"  # pylint: disable=invalid-name

# Every URL of the API (endpoints, schema and docs) requires `basic_access`
api_patterns, api_app_name, api_namespace = api.urls
api_patterns = decorate_url_patterns(
    (api_patterns, api_app_name), basic_access_required
)[0]

urlpatterns = [
    # -- API System
    re_path(r"^api/", (api_patterns, api_app_name, api_namespace)),
    # -- React Frontend, all other routes are handled by the router
    path("", react_base, name="index"),
    re_path(r"^(?!api/).*$", react_base, name="react_base"),
]
