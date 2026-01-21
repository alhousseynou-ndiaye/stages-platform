from django.urls import path
from . import views

urlpatterns = [
    path("", views.offre_list, name="offre_list"),
    path("new/", views.offre_create, name="offre_create"),
    path("<int:pk>/", views.offre_detail, name="offre_detail"),
    path("<int:pk>/archive/", views.offre_archive, name="offre_archive"),
]
