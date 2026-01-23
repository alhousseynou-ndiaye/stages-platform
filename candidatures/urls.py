from django.urls import path
from . import views

urlpatterns = [
    path("postuler/<int:offre_id>/", views.postuler, name="postuler"),
    path("mes/", views.mes_candidatures, name="mes_candidatures"),
    path("offre/<int:offre_id>/", views.candidatures_offre, name="candidatures_offre"),
    path("update-statut/<int:pk>/", views.candidature_update_statut, name="candidature_update_statut"),

]
