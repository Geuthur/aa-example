# Django
from django.template.defaulttags import register

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# AA Example
from example import __title__, __version__

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


@register.simple_tag
def example_templatetag() -> str | None:
    """Example template tag."""
    return "Hello, World!"
