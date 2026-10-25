"""App URLs"""

# Django
from django.urls import path, re_path

# AA Example
from example.api import api
from example.views import react_base

app_name: str = "example"  # pylint: disable=invalid-name

urlpatterns = [
    # -- API System
    re_path(r"^api/", api.urls),
    # -- React Frontend, all other routes are handled by the router
    path("", react_base, name="index"),
    re_path(r"^(?!api/).*$", react_base, name="react_base"),
]
