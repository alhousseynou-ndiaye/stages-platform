from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from offres.models import OffreStage
from .forms import CandidatureCreateForm
from .models import Candidature


def is_etudiant(u):
    return u.is_authenticated and getattr(u, "actif", True) and u.role == User.Role.ETUDIANT


@login_required
@user_passes_test(is_etudiant)
def postuler(request, offre_id):
    offre = get_object_or_404(OffreStage, pk=offre_id, statut="PUBLIEE")

    # évite double candidature
    if Candidature.objects.filter(offre=offre, etudiant=request.user).exists():
        messages.warning(request, "Vous avez déjà postulé à cette offre.")
        return redirect("offre_detail", pk=offre.pk)

    if request.method == "POST":
        form = CandidatureCreateForm(request.POST, request.FILES)
        if form.is_valid():
            cand = form.save(commit=False)
            cand.offre = offre
            cand.etudiant = request.user
            cand.save()
            messages.success(request, "Candidature envoyée avec succès.")
            return redirect("mes_candidatures")
        messages.error(request, "Veuillez corriger les erreurs.")
    else:
        form = CandidatureCreateForm()

    return render(request, "candidatures/candidature_form.html", {"offre": offre, "form": form})


@login_required
@user_passes_test(is_etudiant)
def mes_candidatures(request):
    candidatures = (
        Candidature.objects
        .select_related("offre", "offre__entreprise")
        .filter(etudiant=request.user)
        .order_by("-date_candidature")
    )
    return render(request, "candidatures/mes_candidatures.html", {"candidatures": candidatures})


@login_required
def candidatures_offre(request, offre_id):
    """
    Accès:
    - ADMIN / RESP_PEDAGO: toutes les candidatures
    - ENTREPRISE: seulement si l'offre lui appartient (à implémenter si tu relies entreprise<->user)
    Pour l'instant: ADMIN/RESP seulement.
    """
    u = request.user
    if not (u.role in [User.Role.ADMIN, User.Role.RESP_PEDAGO]):
        return redirect("offre_detail", pk=offre_id)

    offre = get_object_or_404(OffreStage, pk=offre_id)
    candidatures = (
        Candidature.objects
        .select_related("etudiant")
        .filter(offre=offre)
        .order_by("-date_candidature")
    )
    return render(request, "candidatures/candidatures_offre.html", {"offre": offre, "candidatures": candidatures})
