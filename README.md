# 🎓 Plateforme de Gestion et d’Analyse des Offres de Stage

Projet académique développé avec Django dans le cadre du Master 1 Informatique – Data Science.

Cette application permet de centraliser la gestion des entreprises partenaires, des offres de stage, des candidatures étudiantes, des conventions de stage et des statistiques associées.

---

## 📌 Fonctionnalités principales

### 👤 Gestion des utilisateurs
- Authentification sécurisée
- Gestion des rôles : Administrateur, Responsable pédagogique, Étudiant, Entreprise
- Gestion des sessions

### 🏢 Gestion des entreprises
- Création, modification et consultation des entreprises partenaires
- Gestion des contacts
- Recherche avancée (nom, secteur, ville, statut)
- Historique des offres

### 📄 Gestion des offres de stage
- Publication et archivage des offres
- Recherche multicritère
- Filtres avancés
- Téléversement de pièces jointes
- Liaison avec filières

### 📩 Gestion des candidatures
- Dépôt de CV et lettre de motivation
- Suivi du statut
- Notifications
- Accusé de réception
- Génération automatique des conventions

### 📑 Conventions de stage
- Génération automatique au format PDF
- Téléchargement sécurisé
- Suivi de signature

### 📊 Statistiques et tableaux de bord
- Indicateurs clés (KPI)
- Graphiques interactifs
- Taux de placement
- Entreprises les plus actives
- Analyse par filière

### 🔐 Sécurité et journalisation
- Hashage des mots de passe
- Contrôle des accès
- Journal des actions (logs)

---

## 🛠️ Technologies utilisées

- Python 3.11+
- Django 6.0
- SQLite
- HTML / CSS
- Chart.js
- ReportLab (PDF)
- Git / GitHub

---


---

## 🚀 Installation et lancement

### 1️⃣ Cloner le projet

```bash
git clone <URL_DU_REPO>
cd stages_platform


2️⃣ Créer l’environnement virtuel
python -m venv .venv


Activation :

Windows :

.venv\Scripts\activate


Linux / Mac :

source .venv/bin/activate

3️⃣ Installer les dépendances
pip install -r requirements.txt


Si le fichier n’existe pas :

pip install django reportlab

4️⃣ Appliquer les migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Créer un superutilisateur
python manage.py createsuperuser

6️⃣ Lancer le serveur
python manage.py runserver

7️⃣ Accès à l’application
Fonction	URL
Accueil / Dashboard	http://127.0.0.1:8000/

Administration	http://127.0.0.1:8000/admin

Offres	http://127.0.0.1:8000/offres

Entreprises	http://127.0.0.1:8000/entreprises

Candidatures	http://127.0.0.1:8000/candidatures
📊 Données de démonstration

Pour visualiser correctement le dashboard, il est recommandé de créer :

Plusieurs entreprises

Plusieurs offres

Plusieurs candidatures avec statuts variés

Ces données peuvent être ajoutées via l’interface d’administration.




