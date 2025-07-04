"""PvE Views"""

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# AA Example
from example import __title__

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


@login_required
@permission_required("example.basic_access")
def index(request):
    context = {}
    return render(request, "example/index.html", context=context)
