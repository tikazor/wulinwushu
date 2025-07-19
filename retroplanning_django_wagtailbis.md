# Rétroplanning Projet Django + Wagtail (Plateforme Wushu)

## Dernière mise à jour
19 juillet 2025

---

## 🟩 Réalisé (Done)

- **Initialisation du projet**
  - Création de l’environnement virtuel Python.
  - Création du projet Django et de l’app Wagtail (`formation_wushu`).
  - Initialisation des apps : `fiches`, `modules`, `utilisateurs`, etc.
  - Versionning du code localement.

- **Modélisation et migrations**
  - Modèles principaux validés : Fiche, Séquence, Atelier, Technique.
  - Correction des problèmes de migrations et purge d’anciennes migrations bloquantes.
  - Synchronisation entre modèles et admin.

- **Back-office / Admin**
  - Accès admin configuré pour tous les modules.
  - Création du superuser OK.
  - Ajout et gestion des contenus par le back-office.
  - Gestion des droits (is_animateur, superuser, etc.).

- **Fonctionnalités cœur**
  - Création/édition/suppression des Fiches, Séquences, Ateliers, Techniques via formulaires Django.
  - Relations ManyToMany fonctionnelles (Ateliers dans Séquences, Techniques dans Ateliers, Animateurs associés à Fiches, etc.).
  - Navigation et templates principaux mis en place (Deck, boutons d’ajout, affichage détaillé, etc.).
  - Affichage conditionnel et redirection fonctionnelle.
  - Correction des bugs d’association et problèmes liés à l’héritage de Page (Wagtail).

- **Problèmes techniques réglés**
  - Correction des erreurs de migrations liées à Wagtail (migrations manquantes, incompatibilité block_lookup).
  - Suppression et régénération propre des migrations.
  - Résolution des problèmes de sauvegarde ManyToMany sur le modèle FichePage.

---

## 🟨 En cours (Work in progress)

- **Documentation & industrialisation**
  - README.md enrichi : instructions d’utilisation, contexte, technologies, étapes d’installation, TODO, etc.
  - Rétroplanning actualisé.
  - Ajout de commentaires/docstrings sur les fonctions principales.
  - Préparation à la mise en ligne GitHub (arborescence, .gitignore, doc, etc.).

- **Tests & validation**
  - Vérification des workflows utilisateurs (animateur, superuser).
  - Ajout de premiers tests unitaires simples à prévoir (optionnel à ce stade).
  - Scénarios d’ajout/édition/suppression pour chaque modèle.

---

## 🟧 À faire rapidement (Next step)

- **Sauvegarde et versionning distant**
  - Initialiser le repo GitHub, y pousser le projet.
  - Préparer une première version stable (tag v0.1).

- **Base de données PostgreSQL**
  - Adapter les settings Django pour le support PostgreSQL (config locale + prod).
  - Générer le dump/structure pour migration future.
  - Vérifier la compatibilité Wagtail/PostgreSQL.

- **Dockerisation**
  - Ajouter les fichiers Docker nécessaires (Dockerfile, docker-compose.yml).
  - Tester le build et l’exécution locale du stack complet.

- **Industrialisation/Production**
  - Ajout d’un fichier .env d’exemple.
  - Préparer la doc d’installation (README) pour install rapide via Docker.

---

## 🟥 Plus tard / évolutif (Backlog/MVP+)

- Ajout d’un module d’import/export CSV/Excel pour les fiches et séances.
- Améliorations visuelles (tailwind avancé, tableaux, search, etc.).
- Authentification avancée, gestion des rôles plus fine.
- API REST pour accès tiers (applis mobiles, etc.).
- Gestion des médias/documents partagés.
- Rédaction de tests unitaires complets.
- Monitoring, sécurité, backup.

---

## ⏱️ Frise temporelle indicative

| Étape | Objectif | Date estimée |
|-------|----------|--------------|
| ⚡ Initialisation (env, base, apps) | Projet fonctionnel, premier CRUD | Déjà fait |
| 🛠️ Finalisation modèles & migrations | Migrations stables, workflows CRUD OK | Déjà fait |
| 🗄️ Versionning GitHub | Premier commit public | Juillet 2025 |
| 🗃️ PostgreSQL & Dockerisation | Projet industrialisable | Juillet 2025 |
| 🚀 Première version stable | Prêt à déployer et documenté | Juillet 2025 |
| 🌱 Améliorations continues | Fonctions avancées, feedback utilisateurs | Août 2025 et + |

---

### Synthèse

- **Le projet est mature pour un premier dépôt GitHub** et une bascule sur une base de données PostgreSQL/Docker.
- Tous les blocages critiques côté migrations et modèles sont levés.
- Les workflows principaux sont fonctionnels côté utilisateurs (création, édition, suppression, association des objets).
- Quelques points de doc et d’industrialisation restent à finaliser, mais l’ensemble est prêt à être partagé/testé sur une instance collaborative.

---

*Dernière mise à jour : 19/07/2025*
