# Django
from django.db import models
from django.utils.translation import gettext_lazy as _


class General(models.Model):
    """General model for app permissions"""

    class Meta:
        abstract = True  # Please Remove this to activate this model
        managed = False
        permissions = (
            ("basic_access", _("Can access this app, Example")),
            ("manage_access", _("Can manage Example")),
        )
        default_permissions = ()  # Remove standard permissions
