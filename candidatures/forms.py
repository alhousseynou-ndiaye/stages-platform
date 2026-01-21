from django import forms
from .models import Candidature

class CandidatureCreateForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ["cv", "lm", "message"]
