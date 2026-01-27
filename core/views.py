import json
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q
from django.shortcuts import render

from accounts.models import User
from offres.models import OffreStage, Filiere
from candidatures.models import Candidature
from entreprises.models import Entreprise


@login_required
def dashboard(request):
    u = request.user
    if u.role not in [User.Role.ADMIN, User.Role.RESP_PEDAGO]:
        # pas d'accès aux stats
        return render(request, "core/forbidden.html", status=403)

    # KPI de base
    nb_offres = OffreStage.objects.count()
    nb_candidatures = Candidature.objects.count()

    nb_acceptees = Candidature.objects.filter(statut="ACCEPTEE").count()
    taux_acceptation = round((nb_acceptees / nb_candidatures) * 100, 2) if nb_candidatures else 0

    duree_moy = OffreStage.objects.aggregate(m=Avg("duree_mois"))["m"] or 0
    remun_moy = OffreStage.objects.filter(remuneration__isnull=False).aggregate(m=Avg("remuneration"))["m"] or 0

    # Offres par filière
    offres_par_filiere = (
        OffreStage.objects
        .values("filiere_cible__nom")
        .annotate(n=Count("id"))
        .order_by("-n")
    )
    labels_filiere = [x["filiere_cible__nom"] or "Non renseigné" for x in offres_par_filiere]
    data_filiere = [x["n"] for x in offres_par_filiere]

    # Candidatures par statut
    cand_par_statut = (
        Candidature.objects
        .values("statut")
        .annotate(n=Count("id"))
        .order_by("-n")
    )
    labels_statut = [x["statut"] for x in cand_par_statut]
    data_statut = [x["n"] for x in cand_par_statut]

    # Entreprises les plus actives (offres publiées)
    entreprises_actives = (
        OffreStage.objects
        .values("entreprise__raison_sociale")
        .annotate(n=Count("id"))
        .order_by("-n")[:10]
    )
    labels_ent = [x["entreprise__raison_sociale"] for x in entreprises_actives]
    data_ent = [x["n"] for x in entreprises_actives]

    # KPI “placement” simplifié : candidatures acceptées / candidatures
    # (Tu peux l'appeler "taux d’acceptation" dans le rapport)
    context = {
        "nb_offres": nb_offres,
        "nb_candidatures": nb_candidatures,
        "taux_acceptation": taux_acceptation,
        "duree_moy": round(float(duree_moy), 2) if duree_moy else 0,
        "remun_moy": round(float(remun_moy), 2) if remun_moy else 0,

        # JSON pour Chart.js
        "labels_filiere": json.dumps(labels_filiere),
        "data_filiere": json.dumps(data_filiere),

        "labels_statut": json.dumps(labels_statut),
        "data_statut": json.dumps(data_statut),

        "labels_ent": json.dumps(labels_ent),
        "data_ent": json.dumps(data_ent),

        "top_entreprises": entreprises_actives,
    }
    return render(request, "core/dashboard.html", context)
