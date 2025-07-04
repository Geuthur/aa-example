# Django
from django.db import models

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# AA Example
from example import __title__

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


class ExampleQuerySet(models.QuerySet):
    pass


class ExampleManagerBase(models.Manager):
    pass


ExampleManager = ExampleManagerBase.from_queryset(ExampleQuerySet)
