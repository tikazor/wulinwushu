# fiches/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import FichePageForm, SequenceForm, AtelierForm, TechniqueForm
from home.models import HomePage
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from fiches.models import FichePage, Sequence

def is_animateur(user):
    return user.is_authenticated and (getattr(user, "role", "") == "animateur" or user.is_superuser)

# admin_views.py


@staff_member_required
def dashboard_admin(request):
    nb_fiches_a_valider = FichePage.objects.filter(is_public=False).count()
    nb_sequences = Sequence.objects.count()
    # ... Ajoute d'autres stats utiles

    return render(request, "admin/dashboard.html", {
        "nb_fiches_a_valider": nb_fiches_a_valider,
        "nb_sequences": nb_sequences,
    })


def ma_vue(request):
    # Exemples :
    messages.success(request, "La fiche a bien été validée !")
    messages.error(request, "Accès refusé : vous n’avez pas les droits.")
    messages.info(request, "Nouveau module bientôt disponible.")

# Création de séance (fiche)
@login_required
@user_passes_test(is_animateur)
def creer_fiche(request):
    if request.method == "POST":
        form = FichePageForm(request.POST)
        if form.is_valid():
            fiche = form.save(commit=False)
            fiche.owner = request.user  # Si tu utilises ce champ
            fiche.save()                # 1️⃣ Création de la page (et du page_ptr)
            form.save_m2m()             # 2️⃣ Ensuite, tu ajoutes les M2M
            return redirect('liste_seances')
    else:
        form = FichePageForm()
    return render(request, "fiches/form_fiche.html", {"form": form})


# Création de séquence
@login_required
@user_passes_test(is_animateur)
def creer_sequence(request):
    if request.method == "POST":
        form = SequenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_sequences')
    else:
        form = SequenceForm()
    return render(request, "fiches/form_sequence.html", {"form": form})

# Création d'atelier
@login_required
@user_passes_test(is_animateur)
def creer_atelier(request):
    if request.method == "POST":
        form = AtelierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_ateliers')
    else:
        form = AtelierForm()
    return render(request, "fiches/form_atelier.html", {"form": form})

# Création de technique (avec gestion fichiers)
@login_required
@user_passes_test(is_animateur)
def creer_technique(request):
    if request.method == "POST":
        form = TechniqueForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_techniques')
    else:
        form = TechniqueForm()
    return render(request, "fiches/form_technique.html", {"form": form})
