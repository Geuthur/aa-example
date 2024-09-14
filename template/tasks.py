"""App Tasks"""

from celery import shared_task

from template.hooks import get_extension_logger

logger = get_extension_logger(__name__)


@shared_task
def update_all_template():
    """Update all template."""
    # pylint: disable=unnecessary-pass
    pass
