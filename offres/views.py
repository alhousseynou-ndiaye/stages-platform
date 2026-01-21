from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import OffreStageForm, PieceJointeFormSet
from .models import OffreStage


@login_required
def offre_list(request):
    q = request.GET.get("q", "").strip()
    filiere = request.GET.get("filiere", "").strip()
    lieu = request.GET.get("lieu", "").strip()
    remunere = request.GET.get("remunere", "").strip()  # "1" ou ""
    duree_min = request.GET.get("duree_min", "").strip()
    duree_max = request.GET.get("duree_max", "").strip()
    statut = request.GET.get("statut", "").strip()

    offres = OffreStage.objects.select_related("entreprise", "filiere_cible").all()

    # Recherche mots clés (titre/desc/missions/profil/entreprise/lieu)
    if q:
        offres = offres.filter(
            Q(titre__icontains=q) |
            Q(description__icontains=q) |
            Q(missions__icontains=q) |
            Q(profil_recherche__icontains=q) |
            Q(entreprise__raison_sociale__icontains=q) |
            Q(lieu__icontains=q)
        )

    # Filtres
    if filiere:
        offres = offres.filter(filiere_cible__id=filiere)
    if lieu:
        offres = offres.filter(lieu__icontains=lieu)
    if remunere == "1":
        offres = offres.filter(remunere=True)
    if statut:
        offres = offres.filter(statut=statut)

    # Durée min/max
    if duree_min.isdigit():
        offres = offres.filter(duree_mois__gte=int(duree_min))
    if duree_max.isdigit():
        offres = offres.filter(duree_mois__lte=int(duree_max))

    # Tri + pagination
    sort = request.GET.get("sort", "date_publication")
    dir_ = request.GET.get("dir", "desc")
    allowed = {"date_publication", "duree_mois", "remuneration", "lieu", "titre", "statut"}
    if sort in allowed:
        order = f"-{sort}" if dir_ == "desc" else sort
        offres = offres.order_by(order)

    paginator = Paginator(offres, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "offres/offre_list.html", {
        "page_obj": page_obj,
        "q": q,
        "filiere": filiere,
        "lieu": lieu,
        "remunere": remunere,
        "duree_min": duree_min,
        "duree_max": duree_max,
        "statut": statut,
        "sort": sort,
        "dir": dir_,
    })


@login_required
def offre_detail(request, pk):
    offre = get_object_or_404(OffreStage.objects.select_related("entreprise", "filiere_cible"), pk=pk)
    return render(request, "offres/offre_detail.html", {"offre": offre})


@login_required
def offre_create(request):
    # Version simple pour l’instant : tout utilisateur connecté peut créer
    # On restreindra par rôle après (Admin/Entreprise)
    if request.method == "POST":
        form = OffreStageForm(request.POST)
        if form.is_valid():
            offre = form.save()
            formset = PieceJointeFormSet(request.POST, request.FILES, instance=offre)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Offre publiée avec succès.")
                return redirect("offre_detail", pk=offre.pk)
            offre.delete()
            messages.error(request, "Erreur dans les pièces jointes.")
        else:
            messages.error(request, "Veuillez corriger les erreurs.")
            formset = PieceJointeFormSet(request.POST, request.FILES)
    else:
        form = OffreStageForm()
        formset = PieceJointeFormSet()

    return render(request, "offres/offre_form.html", {"form": form, "formset": formset})


@login_required
def offre_archive(request, pk):
    # Archivage simple
    offre = get_object_or_404(OffreStage, pk=pk)
    offre.statut = "ARCHIVEE"
    offre.save(update_fields=["statut"])
    messages.success(request, "Offre archivée.")
    return redirect("offre_detail", pk=offre.pk)
