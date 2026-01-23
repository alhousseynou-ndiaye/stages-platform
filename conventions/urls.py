from django.urls import path
from . import views

urlpatterns = [
    path("generate/<int:candidature_id>/", views.generate_convention, name="generate_convention"),
]
