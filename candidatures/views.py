from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from offres.models import OffreStage
from .forms import CandidatureCreateForm
from .models import Candidature

from django.utils import timezone
from core.models import Log



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


@login_required
def candidature_update_statut(request, pk):
    u = request.user
    if u.role not in [User.Role.ADMIN, User.Role.RESP_PEDAGO]:
        return redirect("mes_candidatures")

    cand = get_object_or_404(Candidature.objects.select_related("offre"), pk=pk)

    if request.method == "POST":
        new_statut = request.POST.get("statut", "").strip()
        allowed = {choice[0] for choice in Candidature.Statut.choices}
        if new_statut not in allowed:
            messages.error(request, "Statut invalide.")
            return redirect("candidatures_offre", offre_id=cand.offre_id)

        cand.statut = new_statut
        cand.date_reponse = timezone.now()
        cand.save(update_fields=["statut", "date_reponse"])

        # Log (notification simulée)
        Log.objects.create(
            user=u,
            action="CHANGEMENT_STATUT_CANDIDATURE",
            details=f"Candidature #{cand.id} -> {new_statut} (Offre #{cand.offre_id})",
        )

        messages.success(request, f"Statut mis à jour : {new_statut}")
        return redirect("candidatures_offre", offre_id=cand.offre_id)

    return redirect("candidatures_offre", offre_id=cand.offre_id)
