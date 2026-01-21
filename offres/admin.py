from django.contrib import admin
from .models import Filiere, OffreStage, PieceJointeOffre

@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ("code", "nom", "niveau")
    search_fields = ("code", "nom", "niveau")

class PieceJointeInline(admin.TabularInline):
    model = PieceJointeOffre
    extra = 1

@admin.register(OffreStage)
class OffreStageAdmin(admin.ModelAdmin):
    list_display = ("titre", "entreprise", "lieu", "duree_mois", "statut", "date_publication")
    list_filter = ("statut", "lieu", "remunere", "filiere_cible")
    search_fields = ("titre", "entreprise__raison_sociale", "lieu")
    inlines = [PieceJointeInline]

@admin.register(PieceJointeOffre)
class PieceJointeOffreAdmin(admin.ModelAdmin):
    list_display = ("offre", "label", "fichier")
