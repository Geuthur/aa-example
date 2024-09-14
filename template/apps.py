"""App Configuration"""

# Django
from django.apps import AppConfig

# AA Example App
from template import __version__


class TemplateConfig(AppConfig):
    """App Config"""

    default_auto_field = "django.db.models.AutoField"
    author = "Geuthur"
    name = "template"
    label = "template"
    verbose_name = f"Template v{__version__}"
