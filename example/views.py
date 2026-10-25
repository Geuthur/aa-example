"""Views: the React entry point."""

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

# AA Example
from example import __app_name__, __version__
from example.models import General


@login_required
@permission_required(General.get_perm(General.Permission.BASIC_ACCESS))
def react_base(request: WSGIRequest):
    """Serve the React app; routing and permissions of the pages are handled by the API."""
    context = {"version": __version__, "app_name": __app_name__}
    return render(request, "example/react_base.html", context=context)
