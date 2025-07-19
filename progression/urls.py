# progression/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("global/", views.tableau_suivi_global, name="suivi_global"),
    path("filtre/", views.tableau_suivi_filtre, name="suivi_filtre"),
    path("valider/<int:fiche_id>/", views.valider_fiche, name="valider_fiche"),

]
