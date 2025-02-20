# Django
from django.db import models

# AA Voices of War
from example.hooks import get_extension_logger

logger = get_extension_logger(__name__)


class ExampleQuerySet(models.QuerySet):
    pass


class ExampleManagerBase(models.Manager):
    pass


ExampleManager = ExampleManagerBase.from_queryset(ExampleQuerySet)
