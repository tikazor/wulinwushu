# 🐍 Projet Django + Wagtail — Plateforme de Formation Wushu

## 🎯 Objectif
Développer une plateforme de formation interactive à destination des animateurs de cours de wushu et de leurs pratiquants.

## 🛠️ Stack Technique
- Backend : Django + Wagtail CMS
- Frontend : Templates Wagtail + Tailwind CSS
- Base de données : PostgreSQL / SQLite (dev)
- Hébergement : Docker sur NAS
- Stockage médias : Volume partagé NAS
- Éditeur : Visual Studio Code

MAJ 14/07/2025
🐍 Projet Django + Wagtail — Plateforme de Formation Wushu
✅ État d'avancement par Jalon
#	Jalon	Détail	Statut	Observation
1	🗂️ Planification & structuration	Cahier des charges, modélisation fiches → séquences → ateliers	✅ Terminé	OK
2	🔐 Authentification & gestion utilisateurs	Système rôles pratiquant/animateur, page de connexion fonctionnelle	✅ Terminé	Connexion, logout, permissions en place
3	📚 Fiches & modules (CMS Wagtail)	Modèles FichePage, Séquence, Atelier, Technique	✅ Terminé	Création via Wagtail OK
4	📈 Suivi progression	Validation fiche, suivi global + filtre animateur	✅ Terminé	Routes /suivi/global & /suivi/filtre fonctionnelles
5	🧩 Interactivité (quiz, commentaires)	Quiz QCM/VraiFaux, retour utilisateur	⏸️ En pause	Mise en attente (repris après jalon 6 ou 10)
6	🧭 Interface & navigation	Menu haut avec rôles, espace perso, responsive	🛠️ En cours	Menu HTML en place, à finaliser selon Tailwind/UX
7	🐳 Dockerisation locale	Dockerfile prêt, docker-compose.yml à créer	🚧 À faire	Non démarré
8	🏠 Déploiement sur NAS	Nginx/gunicorn, volumes médias	🚧 À faire	En attente de Dockerisation
9	🧪 Tests & contenu de démo	Données fictives, tests bout en bout	🚧 À faire	Dépend des jalons 5 et 6
10	📘 Documentation & maintenance	Explication de la structure, guides, maintenance	🚧 À faire	README à enrichir avec déploiement & structure Wagtail

## 🧱 Préparation Production

### 🔄 Base de données
- Migration depuis SQLite vers PostgreSQL prévue via `pgloader` ou script custom.
- Conteneur PostgreSQL dans `docker-compose.yml`

### 🚀 Déploiement
- Code versionné sur GitHub (accès privé)
- Utilisation de GitHub Actions pour build automatique
- NAS : accès via reverse proxy (Nginx), ouverture port 8000/443
- Gestion des médias via volume monté

### 🔧 Performance & sécurité
- PostgreSQL → meilleure gestion multi-accès
- Session & authentification via cookies sécurisés (HTTPS)
- Prévu pour ~50 connexions simultanées (en interne)

### 🔐 À prévoir
- Supervision basique (log errors)
- Sauvegarde automatique de la base
- Séparation environnements dev/prod (fichiers `.env`)


⏭️ Prochaines étapes (Jalon 6 à poursuivre)
 Menu dynamique avec rôles (accès /espace, /suivi/, logout/login)

 Intégration Tailwind CSS (optionnel mais recommandé)

 Ajout d’un logo Wulin en haut ou barre latérale

 Ajout d’un layout pour / + pages Wagtail simples

🕒 Estimation restante
Étape	Durée estimée
Fin interface/navigation	2 jours
Interactivité (quiz/commentaires)	3 jours
Dockerisation & test local	1,5 jours
Déploiement sur NAS	2,5 jours
Contenu test + doc complète	1,5 jours
Total estimé	~10 jours effectifs

MAJ 13/07/2025
## 📦 Structure du projet

formation_wushu/
├── home/
├── fiches/
├── modules/
├── progression/
├── utilisateurs/
├── static/
├── media/
├── templates/
├── formation_wushu/
├── manage.py
└── README.md

## 📅 Rétroplanning

| Jalon                             | Statut |
|----------------------------------|--------|
| Planification & structuration    | ☑ Terminé |
| Auth & gestion utilisateurs      | ☑ Terminé |
| CMS : fiches & modules (Wagtail) | ☑ Terminé |
| Progression & validation         | ☑ Terminé |
| Interactivité (quiz, commentaires)| ☐ Non commencé |
| Interface / navigation           | ☐ Non commencé |
| Dockerisation locale             | ☐ Non commencé |
| Déploiement NAS & médias         | ☐ Non commencé |
| Tests & contenu démo             | ☐ Non commencé |
| Documentation + maintenance      | ☐ Non commencé |

## ✅ MVP - Objectifs Fonctionnels

- [x] Authentification animateur & pratiquant
- [x] Création de fiches pédagogiques
- [x] Organisation en modules
- [x] Validation par les pratiquants
- [x] Suivi par les animateurs
- [ ] Déploiement sur NAS

## 🧪 Environnement de dev

1. `python3 -m venv env`
2. `source env/bin/activate`
3. `pip install -r requirements.txt`
4. `python manage.py runserver`

from pathlib import Path

project_summary_md = """
# 🐍 Projet Django + Wagtail — Plateforme de Formation Wushu

## 🎯 Objectif
Développer une plateforme interactive pour les animateurs et pratiquants de cours de Wushu, avec :
- Création/consultation de fiches pédagogiques structurées
- Validation et suivi des progrès
- Quiz/commentaires
- Hébergement sur NAS via Docker
- Suivi utilisateur, navigation claire, et interface soignée

---

## ✅ Bilan global

### 📁 Structure du projet
- Projet structuré dans `C:/Users/Predator/Documents/Wagtail_wushu`
- Organisation modulaire claire : `fiches/`, `progression/`, `utilisateurs/`, etc.
- Environnement virtuel Python actif
- Fichiers essentiels présents : `requirements.txt`, `Dockerfile`, `manage.py`, `settings/`
- CMS Wagtail installé et configuré

---

## ✅ Jalon 1 : Planification & Structuration
- Cahier des charges structuré
- Modules et relations définis (fiches → séquences → ateliers → techniques)
- Objectifs du MVP listés

✅ **Terminé**

---

## ✅ Jalon 2 : Authentification & Gestion Utilisateurs
- Rôles animateur/pratiquant envisagés
- Authentification opérationnelle

✅ **Terminé (MVP OK)**

---

## ✅ Jalon 3 : Fiches pédagogiques & modules
- Modèles `FichePage`, `Séquence`, `Atelier`, `Technique` créés
- Templates personnalisés
- Création de contenus via Wagtail OK

✅ **Terminé**

---

## ✅ Jalon 4 : Progression & validation
- Modèle `ValidationFiche` fonctionnel
- Bouton de validation opérationnel
- Affichage ✔ ou bouton selon utilisateur
- Pages `/suivi/global/` et `/suivi/filtre/` fonctionnelles

✅ **Terminé**

---

## 🔜 Étapes restantes

### Jalon 5 : Interactivité (quiz, commentaires)
- Quiz simples (QCM ou vrai/faux)
- Saisie des retours utilisateurs

**⏱️ Estimation : 3 jours**

---

### Jalon 6 : Interface & navigation
- Menus selon rôles
- Mise en page avec Tailwind ou Wagtail Templates
- Page d'accueil

**⏱️ Estimation : 2,5 jours**

---

### Jalon 7 : Dockerisation locale
- Dockerfile déjà en place ✅
- docker-compose.yml à créer
- Tests conteneur

**⏱️ Estimation : 1,5 jours**

---

### Jalon 8 : Déploiement sur NAS
- Serveur web NAS (nginx/gunicorn)
- Partage médias
- Test réseau/ports

**⏱️ Estimation : 2,5 jours**

---

### Jalon 9 : Tests & démo
- Saisir des fiches test
- Créer utilisateurs fictifs
- Vérifier permissions

**⏱️ Estimation : 1 jour**

---

### Jalon 10 : Documentation & maintenance
- README enrichi
- Explication structure, routes, rôles
- Consignes de maintenance

**⏱️ Estimation : 1 jour**

---

## 🧠 Profil de développement
- Niveau intermédiaire autodidacte
- À l’aise avec Django, terminal, VS Code
- Bon appui sur l’IA
- Travaille par jalon clair avec MVP progressif

### 🕒 Temps final estimé
En travaillant seul à raison de 2 à 4 h/jour :
**≈ 11 à 12 jours effectifs → soit 2 à 3 semaines de finalisation**

---

## 🔄 Redémarrer le projet

```bash
python manage.py runserver
