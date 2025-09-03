"""PvE Views"""

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# AA Example
from example import __title__, tasks

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


@login_required
@permission_required("example.basic_access")
def index(request):
    """Index View"""
    context = {
        "title": "Example",
    }
    return render(request, "example/index.html", context=context)


@login_required
@permission_required("example.basic_access")
def admin(request: WSGIRequest):
    if not request.user.is_superuser:
        messages.error(request, _("You do not have permission to access this page."))
        return redirect("example:index")

    if request.method == "POST":
        force_refresh = False
        if request.POST.get("force_refresh", False):
            force_refresh = True
        if request.POST.get("run_clear_etag"):
            messages.info(request, _("Queued Clear All ETags"))
            tasks.example_task.apply_async(
                kwargs={"force_refresh": force_refresh}, priority=1
            )
        if request.POST.get("run_update"):
            messages.info(request, _("Queued Update Task"))
            tasks.update_task.apply_async(
                kwargs={
                    "character_id": request.user.profile.main_character.character_id,
                    "force_refresh": force_refresh,
                },
                priority=1,
            )
    return render(request, "example/admin.html")
