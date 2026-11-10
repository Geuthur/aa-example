"""Helpers for ESI tests with pook."""

# Django
from django.core.cache import cache

ESI_BASE_URL = "https://esi.evetech.net"


def wallet_url(owner) -> str:
    """Return the ESI URL of the wallet of an owner."""
    return f"{ESI_BASE_URL}/characters/{owner.character.character_id}/wallet"


def clear_esi_limits(owner) -> None:
    """Remove the ESI error limit and the wallet bucket of an owner from the cache."""
    cache.delete("esi_error_limit_reset")
    cache.delete(f"esi:bucket:char-wallet:{owner.character.character_id}")
