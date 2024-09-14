# Django
from django.db import models

# AA Voices of War
from template.hooks import get_extension_logger

logger = get_extension_logger(__name__)


class TemplateQuerySet(models.QuerySet):
    pass


class TemplateManagerBase(models.Manager):
    pass


TemplateManager = TemplateManagerBase.from_queryset(TemplateQuerySet)
