"""App Tasks"""

# Third Party
from celery import shared_task

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger
from allianceauth.services.tasks import QueueOnce

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# AA Example
from example import __title__, app_settings
from example.decorators import when_esi_is_available

logger = LoggerAddTag(get_extension_logger(__name__), __title__)

MAX_RETRIES_DEFAULT = 3

# Default params for all tasks.
TASK_DEFAULTS = {
    "time_limit": app_settings.EXAMPLE_TASKS_TIME_LIMIT,
    "max_retries": MAX_RETRIES_DEFAULT,
}

# Default params for tasks that need run once only.
TASK_DEFAULTS_ONCE = {**TASK_DEFAULTS, **{"base": QueueOnce}}

_update_example_params = {
    **TASK_DEFAULTS_ONCE,
    **{"once": {"keys": ["character_id", "force_refresh"], "graceful": True}},
}


@shared_task(**TASK_DEFAULTS_ONCE)
def example_task(runs: int = 0, force_refresh: bool = False):
    runs += runs + 1
    if force_refresh is True:
        logger.info("Force refresh requested.")
        return
    logger.info("Regular refresh requested.")


@shared_task(**_update_example_params)
@when_esi_is_available
def update_task(character_id: int, force_refresh: bool):
    logger.info("Updating Task for %s with %s", character_id, force_refresh)
