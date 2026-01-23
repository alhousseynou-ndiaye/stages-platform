from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_convention_pdf(output_path: Path, data: dict):
    """
    Génère un PDF très simple (suffisant pour un projet académique).
    data: dict avec les infos étudiant/entreprise/offre.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    y = height - 60
    c.setFont("Helvetica-Bold", 16)
    c.drawString(60, y, "CONVENTION DE STAGE")
    y -= 40

    c.setFont("Helvetica", 11)
    lines = [
        f"Établissement : {data.get('etablissement', 'Établissement d’enseignement supérieur')}",
        "",
        f"Étudiant : {data['etudiant_nom']} {data['etudiant_prenom']} ({data['etudiant_email']})",
        f"Offre : {data['offre_titre']}",
        f"Entreprise : {data['entreprise_raison_sociale']}",
        f"Lieu : {data['offre_lieu']}",
        f"Durée : {data['offre_duree_mois']} mois",
        f"Date de début : {data['offre_date_debut']}",
        f"Rémunération : {data.get('offre_remuneration', '-')}",
        "",
        "Signatures :",
        " - Étudiant(e) : ___________________________",
        " - Entreprise : ____________________________",
        " - Responsable pédagogique : _______________",
        "",
        "Document généré automatiquement par la plateforme.",
    ]

    for line in lines:
        c.drawString(60, y, line)
        y -= 16
        if y < 80:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = height - 60

    c.save()
