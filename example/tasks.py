"""App Tasks"""

from celery import shared_task

from example.hooks import get_extension_logger

logger = get_extension_logger(__name__)


@shared_task
def update_all_example():
    """Update all example."""
    # pylint: disable=unnecessary-pass
    pass
