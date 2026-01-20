from django.conf import settings
from django.db import models
from django.utils import timezone
from offres.models import OffreStage

def cv_upload_path(instance, filename):
    return f"candidatures/{instance.etudiant_id}/cv/{filename}"

def lm_upload_path(instance, filename):
    return f"candidatures/{instance.etudiant_id}/lm/{filename}"

class Candidature(models.Model):
    class Statut(models.TextChoices):
        RECUE = "RECUE", "Reçue"
        EN_COURS = "EN_COURS", "En cours"
        ACCEPTEE = "ACCEPTEE", "Acceptée"
        REFUSEE = "REFUSEE", "Refusée"
        CONVENTION_SIGNEE = "CONVENTION_SIGNEE", "Convention signée"

    offre = models.ForeignKey(OffreStage, on_delete=models.CASCADE, related_name="candidatures")
    etudiant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="candidatures")
    date_candidature = models.DateTimeField(default=timezone.now)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.RECUE)
    cv = models.FileField(upload_to=cv_upload_path)
    lm = models.FileField(upload_to=lm_upload_path)
    message = models.TextField(blank=True)
    date_reponse = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("offre", "etudiant")

    def __str__(self):
        return f"{self.etudiant} -> {self.offre} ({self.statut})"
