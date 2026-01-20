from django.contrib import admin
from .models import Entreprise, ContactEntreprise

class ContactInline(admin.TabularInline):
    model = ContactEntreprise
    extra = 1

@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    inlines = [ContactInline]
    list_display = ("code", "raison_sociale", "ville", "secteur_activite", "statut_partenariat")
    search_fields = ("raison_sociale", "ville", "secteur_activite", "code")
    list_filter = ("secteur_activite", "statut_partenariat", "ville")

admin.site.register(ContactEntreprise)
