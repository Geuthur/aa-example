"""
Constants
"""

# Standard Library
import os

# AA Example
from example import __title__, __version__

AA_EXAMPLE_BASE_DIR = os.path.join(os.path.dirname(__file__))
AA_EXAMPLE_STATIC_DIR = os.path.join(AA_EXAMPLE_BASE_DIR, "static", "example")

APP_NAME = "aa-example"

GITHUB_URL = f"https://github.com/geuthur/{APP_NAME}"
USER_AGENT = f"{__title__}/{__version__} (+{GITHUB_URL})"
