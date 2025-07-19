# fiches/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import FichePageForm, SequenceForm, AtelierForm, TechniqueForm
from home.models import HomePage


def is_animateur(user):
    return user.is_authenticated and (getattr(user, "role", "") == "animateur" or user.is_superuser)

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
