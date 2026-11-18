# Third Party
from ninja import NinjaAPI

# Django
from django.conf import settings

# AA Example
from example import __title__
from example.api import character, general
from example.api.auth import BasicAccessAuth

api = NinjaAPI(
    title="Example API",
    version="0.5.0",
    urls_namespace="example:api",
    auth=BasicAccessAuth(),
    openapi_url=settings.DEBUG and "/openapi.json" or "",
)


def setup(ninja_api):
    character.ApiEndpoints(ninja_api)
    general.ApiEndpoints(ninja_api)


# Initialize API endpoints
setup(api)
