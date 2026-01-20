from django.db import models
from django.utils import timezone
from entreprises.models import Entreprise

class Filiere(models.Model):
    code = models.CharField(max_length=30, unique=True)
    nom = models.CharField(max_length=120)
    niveau = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.code} - {self.nom} ({self.niveau})"

class OffreStage(models.Model):
    class Statut(models.TextChoices):
        PUBLIEE = "PUBLIEE", "Publiée"
        ARCHIVEE = "ARCHIVEE", "Archivée"

    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name="offres")
    titre = models.CharField(max_length=200)
    description = models.TextField()
    missions = models.TextField()
    profil_recherche = models.TextField()
    duree_mois = models.PositiveIntegerField()
    date_debut = models.DateField()
    remuneration = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lieu = models.CharField(max_length=150)
    nb_postes = models.PositiveIntegerField(default=1)
    filiere_cible = models.ForeignKey(Filiere, on_delete=models.SET_NULL, null=True, related_name="offres")

    # filtres avancés demandés
    remunere = models.BooleanField(default=False)
    type_stage = models.CharField(max_length=50, blank=True)
    date_limite = models.DateField(null=True, blank=True)

    statut = models.CharField(max_length=10, choices=Statut.choices, default=Statut.PUBLIEE)
    date_publication = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.titre} - {self.entreprise.raison_sociale}"

def offre_piece_jointe_path(instance, filename):
    return f"offres/{instance.offre.id}/pieces/{filename}"

class PieceJointeOffre(models.Model):
    offre = models.ForeignKey(OffreStage, on_delete=models.CASCADE, related_name="pieces_jointes")
    label = models.CharField(max_length=100, blank=True)
    fichier = models.FileField(upload_to=offre_piece_jointe_path)

    def __str__(self):
        return self.label or self.fichier.name
