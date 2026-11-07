"""App Tasks"""

# Third Party
from celery import Task, shared_task

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger
from allianceauth.services.tasks import QueueOnce

# AA Example
from example import __title__, app_settings
from example.models.character import CharacterOwner
from example.providers import AppLogger, retry_task_on_esi_error

logger = AppLogger(get_extension_logger(__name__), __title__)

MAX_RETRIES_DEFAULT = 3

# Default params for all tasks.
TASK_DEFAULTS = {
    "time_limit": app_settings.EXAMPLE_TASKS_TIME_LIMIT,
    "max_retries": MAX_RETRIES_DEFAULT,
}

# Default params for tasks that need bind=True.
TASK_DEFAULTS_BIND = {**TASK_DEFAULTS, **{"bind": True}}
# Default params for tasks that need bind=True and run once only.
TASK_DEFAULTS_BIND_ONCE = {**TASK_DEFAULTS, **{"bind": True, "base": QueueOnce}}
# Default params for tasks that need run once only.
TASK_DEFAULTS_ONCE = {**TASK_DEFAULTS, **{"base": QueueOnce}}
# Default params for tasks that run once per owner and are bound to the task instance.
TASK_DEFAULTS_BIND_ONCE_OWNER = {
    **TASK_DEFAULTS_BIND_ONCE,
    **{"once": {"keys": ["owner_pk"], "graceful": True}},
}


@shared_task(**TASK_DEFAULTS_ONCE)
def update_all_characters(force_refresh: bool = False) -> int:
    """Queue an update for every active character. Returns the number of queued updates."""
    CharacterOwner.objects.disable_characters_with_no_owner()

    owner_pks = list(CharacterOwner.objects.active().values_list("pk", flat=True))
    for owner_pk in owner_pks:
        update_character.apply_async(
            args=[owner_pk], kwargs={"force_refresh": force_refresh}
        )

    logger.info("Queued %s character updates", len(owner_pks))
    return len(owner_pks)


@shared_task(**TASK_DEFAULTS_BIND_ONCE_OWNER)
def update_character(self: Task, owner_pk: int, force_refresh: bool = False) -> bool:
    """
    Update the stale sections of one character.

    ESI outages and limits retry the whole task through `retry_task_on_esi_error`,
    errors of a single section end up in its update status.

    Args:
        owner_pk (int): Primary key of the CharacterOwner to update.
        force_refresh (bool): If True, every section is fetched again.

    Returns:
        bool: True if at least one section was updated, False otherwise.
    """
    try:
        owner = CharacterOwner.objects.select_related("character").get(pk=owner_pk)
    except CharacterOwner.DoesNotExist:
        logger.warning("CharacterOwner with pk %s not found.", owner_pk)
        return False

    if owner.is_orphan:
        logger.info("Character %s is an orphan. Skipping update.", owner)
        return False

    sections = owner.get_sections_to_update(force_refresh=force_refresh)
    if not sections:
        logger.info("No updates needed for %s", owner)
        return False

    with retry_task_on_esi_error(self):
        for section in sections:
            logger.debug("Updating %s for %s", section, owner)
            owner.execute_section(section, force_refresh=force_refresh)

    logger.debug("Executed %s section updates for %s", len(sections), owner)
    return True
