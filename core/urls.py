from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="home"),   # page d'accueil
    path("dashboard/", views.dashboard, name="dashboard"),
]
