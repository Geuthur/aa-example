"""Shared ESI client for Voices of War."""

# Alliance Auth
from esi.clients import EsiClientProvider

# AA Example
from example.constants import USER_AGENT

esi = EsiClientProvider(app_info_text=USER_AGENT)
