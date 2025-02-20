"""App Configuration"""

# Django
from django.apps import AppConfig

# AA Example App
from example import __version__


class ExampleConfig(AppConfig):
    """App Config"""

    default_auto_field = "django.db.models.AutoField"
    author = "Geuthur"
    name = "example"
    label = "example"
    verbose_name = f"Example v{__version__}"
