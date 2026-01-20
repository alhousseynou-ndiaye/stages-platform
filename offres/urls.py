from django.urls import path
from . import views

urlpatterns = [
    path("", views.offres_home, name="offres_home"),
]
