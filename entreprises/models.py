import uuid
from django.db import models

class Entreprise(models.Model):
    class StatutPartenariat(models.TextChoices):
        ACTIF = "ACTIF", "Actif"
        INACTIF = "INACTIF", "Inactif"

    code = models.CharField(max_length=20, unique=True, editable=False)
    raison_sociale = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=120)
    telephone = models.CharField(max_length=30)
    email = models.EmailField()
    site_web = models.URLField(blank=True)
    secteur_activite = models.CharField(max_length=150)
    statut_partenariat = models.CharField(
        max_length=10, choices=StatutPartenariat.choices, default=StatutPartenariat.ACTIF
    )

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f"ENT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.raison_sociale} ({self.code})"

class ContactEntreprise(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name="contacts")
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    fonction = models.CharField(max_length=120)
    telephone = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.entreprise.raison_sociale}"
