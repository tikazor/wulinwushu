from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from utilisateurs.permissions import can_access_tableau_suivi_global, is_animateur
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import get_user_model

from fiches.models import FichePage
from .models import ValidationFiche

User = get_user_model()

def is_animateur(user):
    # On vérifie le rôle via Profile
    profile = getattr(user, "profile", None)
    return user.is_authenticated and profile and profile.role == "animateur"

@login_required(login_url="login")

def tableau_suivi_global(request):

    # Contrôle centralisé de la permission
    if not can_access_tableau_suivi_global(request.user):
        raise PermissionDenied()
    utilisateurs = User.objects.all().order_by("username")
    fiches = FichePage.objects.live().order_by("title")
    data = {
        utilisateur: {
            fiche: ValidationFiche.objects.filter(
                fiche=fiche, utilisateur=utilisateur, valide=True
            ).exists()
            for fiche in fiches
        }
        for utilisateur in utilisateurs
    }
    return render(request, "progression/suivi_global.html", {
        "utilisateurs": utilisateurs,
        "fiches": fiches,
        "data": data,
    })

@login_required(login_url="login")
@user_passes_test(is_animateur, login_url="login")

def tableau_suivi_filtre(request):
    utilisateurs = User.objects.all().order_by("username")
    fiches = FichePage.objects.live().order_by("title")
    validations = ValidationFiche.objects.all()
    fiche_id = request.GET.get("fiche")
    if fiche_id:
        validations = validations.filter(fiche__id=fiche_id)
    utilisateur_id = request.GET.get("utilisateur")
    if utilisateur_id:
        validations = validations.filter(utilisateur__id=utilisateur_id)
    return render(request, "progression/suivi_filtre.html", {
        "validations": validations,
        "utilisateurs": utilisateurs,
        "fiches": fiches,
        "fiche_id": fiche_id,
        "utilisateur_id": utilisateur_id,
    })

@login_required(login_url="login")
def valider_fiche(request, fiche_id):
    fiche = get_object_or_404(FichePage, id=fiche_id)
    vf, created = ValidationFiche.objects.get_or_create(
        fiche=fiche,
        utilisateur=request.user,
        defaults={"valide": True}
    )
    if not created and not vf.valide:
        vf.valide = True
        vf.save()
    messages.success(request, f"Fiche « {fiche.title} » validée avec succès !")
    return redirect(fiche.url)
