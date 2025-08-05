from django.urls import path, include
from modules import views as modules_views
from fiches import views as fiches_views
from utilisateurs import views as utilisateurs_views
from wagtailstreamforms import urls as wagtailstreamforms_urls

urlpatterns = [
    # ... autres patterns
    path("forms/", include(wagtailstreamforms_urls)),
]

urlpatterns = [
    path('', modules_views.liste_modules, name='liste_modules'),

    path('techniques/', modules_views.liste_techniques, name='liste_techniques'),
    path('sequences/', modules_views.liste_sequences, name='liste_sequences'),
    path('ateliers/', modules_views.liste_ateliers, name='liste_ateliers'),
    path('seances/', modules_views.liste_seances, name='liste_seances'),

    path("ateliers/<int:pk>/", modules_views.detail_atelier, name="detail_atelier"),
    path("seances/<int:pk>/", modules_views.detail_seance, name="detail_seance"),
    path("techniques/<int:pk>/", modules_views.detail_technique, name="detail_technique"),
    path("sequences/<int:pk>/", modules_views.detail_sequence, name="detail_sequence"),

    path('fiche/<int:pk>/modifier/', utilisateurs_views.modifier_fiche, name='modifier_fiche'),
    path('fiche/<int:pk>/supprimer/', utilisateurs_views.supprimer_fiche, name='supprimer_fiche'),

    path('creer_fiche/', fiches_views.creer_fiche, name='creer_fiche'),
    path('creer_sequence/', fiches_views.creer_sequence, name='creer_sequence'),
    path('creer_atelier/', fiches_views.creer_atelier, name='creer_atelier'),
    path('creer_technique/', fiches_views.creer_technique, name='creer_technique'),

    # tu peux ajouter ici des vues propres à fiches_views si besoin, exemple :
    # path('fiches_special/', fiches_views.special_fiche, name='special_fiche'),
]