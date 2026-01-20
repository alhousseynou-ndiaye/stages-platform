from django.urls import path
from . import views

urlpatterns = [
    path("", views.candidatures_home, name="candidatures_home"),
]
