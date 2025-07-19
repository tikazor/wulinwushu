from django.urls import path, include
from modules import views as modules_views
from fiches import views 
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

    path('creer_fiche/', views.creer_fiche, name='creer_fiche'),
    path('creer_sequence/', views.creer_sequence, name='creer_sequence'),
    path('creer_atelier/', views.creer_atelier, name='creer_atelier'),
    path('creer_technique/', views.creer_technique, name='creer_technique'),
    path("forms/", include(wagtailstreamforms_urls)),

    # tu peux ajouter ici des vues propres à fiches_views si besoin, exemple :
    # path('fiches_special/', fiches_views.special_fiche, name='special_fiche'),
]