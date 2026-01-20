from django import forms
from django.forms import inlineformset_factory
from .models import Entreprise, ContactEntreprise

class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = [
            "raison_sociale", "adresse", "ville", "telephone", "email",
            "secteur_activite", "site_web", "statut_partenariat",
        ]

class ContactEntrepriseForm(forms.ModelForm):
    class Meta:
        model = ContactEntreprise
        fields = ["nom", "prenom", "fonction", "telephone", "email"]

ContactFormSet = inlineformset_factory(
    Entreprise,
    ContactEntreprise,
    form=ContactEntrepriseForm,
    extra=1,
    can_delete=False,
)
