from pathlib import Path
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from accounts.models import User
from candidatures.models import Candidature
from core.models import Log
from .models import Convention
from .utils import generate_convention_pdf


@login_required
def generate_convention(request, candidature_id):
    u = request.user
    if u.role not in [User.Role.ADMIN, User.Role.RESP_PEDAGO]:
        return redirect("mes_candidatures")

    cand = get_object_or_404(
        Candidature.objects.select_related("offre", "offre__entreprise", "etudiant"),
        pk=candidature_id
    )

    # Crée ou récupère la convention
    convention, _ = Convention.objects.get_or_create(candidature=cand)

    # Chemin fichier
    filename = f"convention_candidature_{cand.id}.pdf"
    rel_path = Path("conventions") / filename
    abs_path = Path(settings.MEDIA_ROOT) / rel_path

    # Données
    data = {
        "etablissement": "Université / École",
        "etudiant_nom": getattr(cand.etudiant, "nom", "") or cand.etudiant.username,
        "etudiant_prenom": getattr(cand.etudiant, "prenom", "") or "",
        "etudiant_email": cand.etudiant.email or "",
        "offre_titre": cand.offre.titre,
        "entreprise_raison_sociale": cand.offre.entreprise.raison_sociale,
        "offre_lieu": cand.offre.lieu,
        "offre_duree_mois": cand.offre.duree_mois,
        "offre_date_debut": cand.offre.date_debut,
        "offre_remuneration": cand.offre.remuneration if cand.offre.remuneration is not None else "-",
    }

    # Génère PDF
    generate_convention_pdf(abs_path, data)

    # Mise à jour convention
    convention.date_generation = timezone.now()
    convention.statut_signature = "EN_ATTENTE"
    convention.document.name = str(rel_path).replace("\\", "/")  # important Windows
    convention.save()

    # Statut candidature (optionnel mais pratique)
    cand.statut = "CONVENTION_SIGNEE"
    cand.date_reponse = timezone.now()
    cand.save(update_fields=["statut", "date_reponse"])

    # Log
    Log.objects.create(
        user=u,
        action="GENERATION_CONVENTION",
        details=f"Convention générée pour Candidature #{cand.id} (Offre #{cand.offre_id})",
    )

    messages.success(request, "Convention générée (PDF).")
    return redirect("candidatures_offre", offre_id=cand.offre_id)
