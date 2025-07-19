✅ Objectif : Tester l’ensemble des fonctionnalités du point de vue utilisateur
1. 🧍‍♂️ Création et test des utilisateurs
Étape	Détail
👤 Crée 3 utilisateurs	via l’admin Django : pratiquant1, animateur1, admin1  ✅ Terminé
🏷️ Attribue leur un rôle personnalisé	pratiquant, animateur, admin selon ton modèle User ou Profile  ✅ Terminé
🔑 Connecte-toi avec chacun	pour vérifier les vues accessibles, menu de navigation, etc.  ✅ Terminé

2. 📄 Création de fiches
Étape	Détail attendu
📝 Crée une ou deux fiches	via l’admin Wagtail (ex: Séance Shaolin 01)  ✅ Terminé
🔗 Ajoute une ou plusieurs séquences	via StreamField  ✅ Terminé
🔗 Dans chaque séquence, ajoute plusieurs ateliers	  ✅ Terminé
⚙️ Vérifie les champs affichés : date, durée, animateurs, participants	  ✅ Terminé

3. 🔁 Test d'affichage dynamique des fiches
Test	Attendu
👁️ Visite une fiche en tant que pratiquant	Page claire, détails visibles  ✅ Terminé
✅ Teste le bouton "Valider cette fiche"	Devrait apparaître, puis disparaître si déjà validée
🔁 Recharge la page	Affiche bien la validation si elle existe

4. 📊 Test des vues de suivi
Page	Rôle	Attendu
/suivi/global/	animateur	Tableau croisé dynamique (qui a validé quoi)
/suivi/filtre/	animateur	Filtre fiche + utilisateur
🧑 Pratiquant	accès interdit à /suivi/ => redirection/login	

5. 🧭 Test des menus et navigation
Élément	Comportement attendu
Barre de navigation (haut ou latérale)	Présente sur toutes les pages
Connexion / Déconnexion	Fonctionnelles
Liens visibles selon rôle	Ex: animateur voit "Suivi", pratiquant ne le voit pas

6. 📱 Test responsive
Test	Détail
Ouvre sur téléphone ou simulateur navigateur mobile	Vérifie affichage adaptatif
Menu lisible	Pas de débordement

❓Tu veux aller plus loin ? Prochaines mini-tâches :
 Créer des tests automatiques (via pytest ou unittest)

 Afficher la progression d’un pratiquant

 Ajouter des champs comme "commentaires" dans une fiche ou un atelier

 Export PDF ou impression d’une fiche

Souhaites-tu que je t’aide à créer :

Un jeu de données de test complet ?

Une checklist interactive à cocher ?

Des modèles de page d’aide/explication pour les utilisateurs ?

Tu peux aussi me demander de générer des cas d’usage à tester pour s’assurer que tout fonctionne comme attendu.