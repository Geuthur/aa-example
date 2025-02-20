"""App URLs"""

from django.urls import path

from example import views

app_name: str = "example"

urlpatterns = [
    path("", views.index, name="index"),
]
