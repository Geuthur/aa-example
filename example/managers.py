# Standard Library
from typing import Generic, TypeVar

# Django
from django.db import models

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter
from allianceauth.services.hooks import get_extension_logger

# AA Example
from example import __title__
from example.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)

T = TypeVar("T", bound=models.Model)


class AccessQuerySet(models.QuerySet[T], Generic[T]):
    """
    A QuerySet with access control methods for the whole Application.

    Methods:
        visible_to(user): Returns objects visible to the given user.
        manage_to(user): Returns objects the given user can manage.
    """

    def visible_to(self, user):
        """Get all objects visible to the user."""
        # superusers get all visible
        if user.is_superuser:
            logger.debug(
                "Returning all objects for superuser %s.",
                user,
            )
            return self

        if user.has_perm("example.full_access"):
            logger.debug("Returning all objects for admin user %s.", user)
            return self

        try:
            char = user.profile.main_character
            assert char
            queries = [models.Q(owner=user)]
            queries.append(models.Q(is_public=True))

            logger.debug("%s queries for user %s visible.", len(queries), user)

            query = queries.pop()
            for q in queries:
                query |= q
            return self.filter(query)
        except AssertionError:
            logger.debug("User %s has no main character. Nothing visible.", user)
            return self.none()

    def manage_to(self, user):
        """Get QuerySet of objects that the user can manage."""
        # superusers get all visible
        if user.is_superuser:
            logger.debug(
                "Returning all manageable queries for superuser %s.",
                user,
            )
            return self

        if user.has_perm("example.full_access"):
            logger.debug("Returning all manageable queries for admin user %s.", user)
            return self

        try:
            char = user.profile.main_character
            assert char
            queries = [models.Q(owner=user)]

            logger.debug("%s queries for user %s manageable.", len(queries), user)

            query = queries.pop()
            for q in queries:
                query |= q
            return self.filter(query)
        except AssertionError:
            logger.debug("User %s has no main character. Nothing manageable.", user)
            return self.none()


class AccessManager(models.Manager[T], Generic[T]):
    """
    A Manager with access control methods for the whole Application

    This manager provides methods to filter querysets based on user permissions,
    such as `visible_to` and `manage_to`, ensuring that users only see or manage
    the objects they are allowed to.
    """

    def get_queryset(self) -> AccessQuerySet[T]:
        return AccessQuerySet(self.model, using=self._db)

    def visible_to(self, user):
        return self.get_queryset().visible_to(user)

    def manage_to(self, user):
        return self.get_queryset().manage_to(user)

    @staticmethod
    def visible_eve_characters(user):
        qs = EveCharacter.objects.get_queryset()
        if user.is_superuser:
            logger.debug("Returning all characters for superuser %s.", user)
            return qs.all()

        if user.has_perm("example.full_access"):
            logger.debug("Returning all characters for %s.", user)
            return qs.all()

        try:
            char = user.profile.main_character
            assert char
            queries = [models.Q(character_ownership__user=user)]

            logger.debug(
                "%s queries for user %s visible chracters.", len(queries), user
            )

            query = queries.pop()
            for q in queries:
                query |= q
            return qs.filter(query)
        except AssertionError:
            logger.debug("User %s has no main character. Nothing visible.", user)
            return qs.none()
