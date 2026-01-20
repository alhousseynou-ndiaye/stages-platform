from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EntrepriseForm, ContactFormSet
from .models import Entreprise

from django.contrib.auth.decorators import user_passes_test
from accounts.permissions import is_admin, is_resp


from django.core.paginator import Paginator

@login_required
def entreprise_list(request):
    q = request.GET.get("q", "").strip()
    secteur = request.GET.get("secteur", "").strip()
    ville = request.GET.get("ville", "").strip()
    statut = request.GET.get("statut", "").strip()

    entreprises = Entreprise.objects.all()

    # Recherche (nom, secteur, ville, code)
    if q:
        entreprises = entreprises.filter(
            Q(raison_sociale__icontains=q) |
            Q(secteur_activite__icontains=q) |
            Q(ville__icontains=q) |
            Q(code__icontains=q)
        )

    # Filtres
    if secteur:
        entreprises = entreprises.filter(secteur_activite__icontains=secteur)
    if ville:
        entreprises = entreprises.filter(ville__icontains=ville)
    if statut:
        entreprises = entreprises.filter(statut_partenariat=statut)

    # Tri par colonnes
    sort = request.GET.get("sort", "raison_sociale")
    direction = request.GET.get("dir", "asc")
    allowed = {"raison_sociale", "ville", "secteur_activite", "statut_partenariat", "code"}

    if sort in allowed:
        order = f"-{sort}" if direction == "desc" else sort
        entreprises = entreprises.order_by(order)

    # Pagination
    paginator = Paginator(entreprises, 10)  # 10 par page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "entreprises/entreprise_list.html",
        {
            "page_obj": page_obj,
            "q": q,
            "secteur": secteur,
            "ville": ville,
            "statut": statut,
            "sort": sort,
            "dir": direction,
        },
    )


@login_required
def entreprise_create(request):
    if request.method == "POST":
        form = EntrepriseForm(request.POST)
        if form.is_valid():
            entreprise = form.save()
            formset = ContactFormSet(request.POST, instance=entreprise)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Entreprise créée avec succès.")
                return redirect("entreprise_detail", pk=entreprise.pk)
            entreprise.delete()
            messages.error(request, "Erreur dans le contact référent.")
        else:
            messages.error(request, "Veuillez corriger les erreurs.")
            formset = ContactFormSet(request.POST)
    else:
        form = EntrepriseForm()
        formset = ContactFormSet()

    return render(request, "entreprises/entreprise_form.html", {"form": form, "formset": formset})


@login_required
def entreprise_detail(request, pk):
    entreprise = get_object_or_404(Entreprise, pk=pk)
    return render(request, "entreprises/entreprise_detail.html", {"entreprise": entreprise})


def is_admin_or_resp(u):
    return is_admin(u) or is_resp(u)

@login_required
@user_passes_test(is_admin_or_resp)
def entreprise_update(request, pk):
    entreprise = get_object_or_404(Entreprise, pk=pk)

    if request.method == "POST":
        form = EntrepriseForm(request.POST, instance=entreprise)
        if form.is_valid():
            form.save()
            messages.success(request, "Entreprise modifiée avec succès.")
            return redirect("entreprise_detail", pk=entreprise.pk)
        messages.error(request, "Veuillez corriger les erreurs.")
    else:
        form = EntrepriseForm(instance=entreprise)

    return render(request, "entreprises/entreprise_update.html", {"form": form, "entreprise": entreprise})
