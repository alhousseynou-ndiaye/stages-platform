from django.urls import path
from . import views

urlpatterns = [
    path("", views.conventions_home, name="conventions_home"),
]
