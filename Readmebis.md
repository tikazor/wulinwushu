Wagtail Wushu – Plateforme de gestion de séances et contenus pédagogiques

📊 Statut du projet

Dernière mise à jour : 18 juillet 2025

Statut : 💪 En développement actif — fin de la phase structure/modèles, prêt pour dockerisation et passage PostgreSQL.

📁 Structure actuelle du projet

Django 5.0 + Wagtail (CMS)

Modules principaux : fiches (séances), séquences, ateliers, techniques, progression, utilisateurs (roles)

Authentification avec rôles : animateur, superadmin

Backoffice Wagtail pour la gestion des contenus + formulaires custom (hors admin) fonctionnels

📝 Jalons du projet

Jalon

Statut

Dernière action/résultat

Structuration & modélisation

✅ Terminé

Modèles stables, migrations ok

Auth & utilisateurs

✅ Terminé

Connexion, rôles, droits

Fiches & modules (CMS)

✅ Terminé

CRUD Wagtail/admin fonctionnel

Progression/validation

✅ Terminé

Tracking progression

Interface/navigation

✅ Terminé

Menu, navigation responsive

Dockerisation locale

🚧 À faire

Prêt à dockeriser

Déploiement NAS/Serveur

🚧 À faire

Attente Docker

Tests & contenu démo

🚧 À faire

À faire après prod

Documentation & maintenance

🚧 À faire

README/Doc à enrichir

Interactivité avancée (quiz...)

⏸ En pause

Prévu après MVP stable

⚡ Actions prioritaires à venir

Commit initial sur GitHub avec structure propre

Ajout fichier .env.example pour la gestion des secrets/envs

Préparation de la BDD PostgreSQL (psycopg2-binary)

Création du Dockerfile + docker-compose.yml pour Django/Postgres/Médias

Test intégral local via Docker, puis déploiement sur NAS

🛠️ Installation / Lancement rapide

1. Dépôts et installation locales (pré-Docker)

Cloner le repo (à compléter après mise en ligne)

Créer le .env à partir du .env.example

Installer requirements :

pip install -r requirements.txt

Lancer les migrations initiales :

python manage.py makemigrations
python manage.py migrate

Créer un superuser :

python manage.py createsuperuser

Lancer le serveur local :

python manage.py runserver

2. Utilisation Docker (préparation)

(À compléter après dockerisation effective)

📦 Roadmap (résumé)



🏷️ Notes

Gestion des migrations : purge OK, base clean (cf. 18/07)

Priorité à la stabilité, test intensif des formulaires et de la navigation

Déploiement NAS → à enclencher dès que Docker local OK

Documentation à enrichir après premier run Docker