from django import forms
from django.forms import inlineformset_factory
from .models import OffreStage, PieceJointeOffre

class OffreStageForm(forms.ModelForm):
    class Meta:
        model = OffreStage
        fields = [
            "entreprise", "titre", "description", "missions", "profil_recherche",
            "duree_mois", "date_debut", "remuneration", "lieu",
            "nb_postes", "filiere_cible", "statut",
            "remunere", "type_stage", "date_limite",
        ]
        widgets = {
            "date_debut": forms.DateInput(attrs={"type": "date"}),
            "date_limite": forms.DateInput(attrs={"type": "date"}),
        }

class PieceJointeOffreForm(forms.ModelForm):
    class Meta:
        model = PieceJointeOffre
        fields = ["label", "fichier"]

PieceJointeFormSet = inlineformset_factory(
    OffreStage,
    PieceJointeOffre,
    form=PieceJointeOffreForm,
    extra=1,
    can_delete=True,
)
