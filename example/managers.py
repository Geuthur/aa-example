# Django
from django.db import models

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Example
from example import __title__
from example.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


class ExampleQuerySet(models.QuerySet):
    pass


class ExampleManagerBase(models.Manager):
    pass


ExampleManager = ExampleManagerBase.from_queryset(ExampleQuerySet)
