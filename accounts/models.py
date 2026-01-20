from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrateur"
        RESP_PEDAGO = "RESP_PEDAGO", "Responsable pédagogique"
        ETUDIANT = "ETUDIANT", "Étudiant"
        ENTREPRISE = "ENTREPRISE", "Entreprise"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ETUDIANT)
    nom = models.CharField(max_length=100, blank=True)
    prenom = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
