from django.db import models
from django.utils import timezone
from candidatures.models import Candidature

def convention_upload_path(instance, filename):
    return f"conventions/{instance.candidature_id}/{filename}"

class Convention(models.Model):
    class StatutSignature(models.TextChoices):
        GENEREE = "GENEREE", "Générée"
        EN_ATTENTE = "EN_ATTENTE", "En attente signature"
        SIGNEE = "SIGNEE", "Signée"

    candidature = models.OneToOneField(Candidature, on_delete=models.CASCADE, related_name="convention")
    date_generation = models.DateTimeField(default=timezone.now)
    statut_signature = models.CharField(
        max_length=15, choices=StatutSignature.choices, default=StatutSignature.GENEREE
    )
    document = models.FileField(upload_to=convention_upload_path)

    def __str__(self):
        return f"Convention {self.candidature_id} ({self.statut_signature})"
