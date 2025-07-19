# 📅 Rétroplanning - Projet Django + Wagtail (Formation Wushu)

Suivi des jalons de développement dans VS Code (format markdown)

| Jalon                              | Date début | Date fin   | Durée (jours) | Statut     | Commentaire                                   |
| ---------------------------------- | ---------- | ---------- | ------------- | ---------- | --------------------------------------------- |
| Planification & structuration      | 2025-07-13 | 2025-07-14 | 2             | ✅ Terminé  | Structure initiale et backlog validé          |
| Auth & gestion utilisateurs        | 2025-07-15 | 2025-07-18 | 4             | ✅ Terminé  | Création profils, espace personnel            |
| CMS : fiches & modules (Wagtail)   | 2025-07-19 | 2025-07-24 | 6             | ✅ Terminé  | Fiches, séquences, ateliers liés              |
| Progression & validation           | 2025-07-25 | 2025-07-28 | 4             | ✅ Terminé  | Système de validation et suivi                |
| Interface / navigation             | 2025-07-29 | 2025-07-30 | 2             | ✅ Terminé  | Header, menus conditionnels, espace personnel |
| Conversion SQLite → PostgreSQL	 | 2025-08-01 |	2025-08-01 | 1             | 🔜 À faire	 | Migration + test structure                      | 
| GitHub Push & CI/CD (pré-prod)	 | 2025-08-02 |	2025-08-02 | 1             | 🔜 À faire	 | Push repo, config Actions ou prébuild automatique| 
| Dockerisation locale               | 2025-08-03 | 2025-08-04 | 2             | 🔜 À faire	 | Intégrer PostgreSQL + médias                    | 
| Déploiement NAS (prod)	         | 2025-08-05 |	2025-08-07 | 3             | 🔜 À faire	 | Préparer prod (ports, accès externe, sécurité)| 
| Préparation montée en charge (prod)| 	2025-08-08	2025-08-08 | 1             | 🔜 À faire	 | Prévoir 50 utilisateurs simultanés, monitoring| 
| Dockerisation locale               | 2025-07-31 | 2025-08-01 | 2             | 🔜 À faire  | À intégrer dès que les bases sont figées      |
| Interactivité (quiz, commentaires) | 2025-08-02 | 2025-08-04 | 3             | ⏸ En pause  | Reporté volontairement après interface        |
| Déploiement NAS & médias           | 2025-08-05 | 2025-08-08 | 4             | 🔜 À faire  | Prévu après dockerisation locale              |
| Tests & contenu démo               | 2025-08-09 | 2025-08-10 | 2             | 🔜 À faire  | Pour valider en conditions réelles            |
| Documentation + maintenance        | 2025-08-11 | 2025-08-12 | 2             | 🔜 À faire  | Finalisation et passation possible            |

# 📌 Fonctionnalités Complémentaires - Triées par Impact

| Fonctionnalité                                                                 | Thématique             | Impact |
|--------------------------------------------------------------------------------|------------------------|--------|
| Suivi de progression détaillé (graphiques, % par utilisateur/module)          | Suivi des apprenants   | 🔥 Élevé |
| Notifications (rappels, nouveautés, validation)                               | Expérience utilisateur | 🔥 Élevé |
| Feedbacks des utilisateurs (notation, commentaires libres)                    | Suivi qualité          | 🔥 Élevé |
| Statistiques de validation et d’activité par module                           | Suivi des apprenants   | 🔥 Élevé |
| Accès multi-rôle (admin, référent, formateur) avec permissions fines          | Gestion des rôles      | 🔥 Élevé |
| Interface utilisateur responsive améliorée (mobile-first)                     | UI/UX                  | 🔥 Élevé |
| Barre de recherche dans les modules/fiches                                    | Navigation             | 🔥 Élevé |
| Génération de certificats de fin de parcours                                  | Suivi des apprenants   | 🔥 Élevé |
| Intégration des médias externes (vidéos, pdf, images, audio)                  | Contenu pédagogique    | 🔥 Élevé |
| Ajout d’étiquettes/tags aux fiches pour faciliter le tri                      | Organisation contenu   | ⚡ Moyen |
| Gestion des rétroliens entre modules/fiches                                   | Organisation contenu   | ⚡ Moyen |
| Impression PDF des fiches/modules                                             | Exportation            | ⚡ Moyen |
| Système de quiz dynamique (drag & drop, QCM, audio)                           | Interactivité          | ⚡ Moyen |
| Chat ou commentaires contextualisés par module                                | Collaboration          | ⚡ Moyen |
| Ajout d’un système de progression gamifié (badges, niveaux)                   | Engagement utilisateur | ⚡ Moyen |
| Import/Export de données utilisateurs en CSV                                  | Admin/gestion          | ⚡ Moyen |
| Tableau de bord personnalisé pour chaque utilisateur                          | Suivi des apprenants   | ⚡ Moyen |
| Ajout de versions multiples d’une même fiche (historique)                     | Gestion contenu        | ⚡ Moyen |
| Traduction multilingue du site                                                | Accessibilité          | 💧 Faible |
| Intégration avec outils externes (Drive, YouTube, etc.)                       | Ressources externes    | 💧 Faible |
| Support de thèmes sombres/clairs                                              | UI/UX                  | 💧 Faible |
| Tutoriels interactifs à l’onboarding                                          | Aide/formation         | 💧 Faible |



✅ Point d'étape :
Tu es actuellement à la fin du Jalon 6, prêt pour démarrer :

Le Jalon 7 - Dockerisation locale

Ou directement le Jalon 8 - Déploiement NAS, selon tes priorités.

Le Jalon 5 (interactivité) est mis en pause volontairement, il pourra être traité en dernier ou après Jalon 10.