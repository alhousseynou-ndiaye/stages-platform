from django.urls import path
from . import views

urlpatterns = [
    path("", views.entreprises_home, name="entreprises_home"),
]
