"""PvE Views"""

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Example
from example import __title__
from example.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


@login_required
@permission_required("example.basic_access")
def index(request):
    """Index View"""
    context = {
        "title": "Example",
    }
    return render(request, "example/view-index.html", context=context)
