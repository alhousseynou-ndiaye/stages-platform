from django.urls import path
from . import views

urlpatterns = [
    path("", views.entreprise_list, name="entreprise_list"),
    path("new/", views.entreprise_create, name="entreprise_create"),
    path("<int:pk>/edit/", views.entreprise_update, name="entreprise_update"),

]
