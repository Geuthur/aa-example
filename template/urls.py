"""App URLs"""

from django.urls import path

from template import views

app_name: str = "template"

urlpatterns = [
    path("", views.index, name="index"),
]
