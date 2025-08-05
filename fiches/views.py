# fiches/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import FichePageForm, SequenceForm, AtelierForm, TechniqueForm
from home.models import HomePage
from django.utils.text import slugify
from wagtail.models import Page
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
    # À ADAPTER : définis ici la page parent des fiches (souvent HomePage ou une page d’index)
    parent_page = Page.objects.get(slug="home")  # Remplace par le slug/id de ta HomePage ou d’une page d’index Fiche

    if request.method == "POST":
        form = FichePageForm(request.POST)
        if form.is_valid():
            fiche = form.save(commit=False)
            # Les champs obligatoires
            fiche.title = form.cleaned_data.get("title", "Fiche sans titre")
            fiche.slug = slugify(fiche.title)
            # Ajout dans l’arborescence Wagtail (important)
            parent_page.add_child(instance=fiche)
            fiche.save_revision().publish()
            form.save_m2m()  # Enregistre les relations ManyToMany (séquences, animateurs, etc.)
            return redirect('liste_seances')
    else:
        form = FichePageForm()

    # Chargement des séquences pour affichage dans le formulaire
    sequences = Sequence.objects.prefetch_related('ateliers__techniques').all().order_by('titre')
    selected_sequences = request.POST.getlist('sequences') if request.method == "POST" else []

    return render(request, "fiches/form_fiche.html", {
        "form": form,
        "sequences": sequences,
        "selected_sequences": [int(s) for s in selected_sequences],
    })



# Création de séquence
@login_required
@user_passes_test(is_animateur)
def creer_sequence(request):
    from modules.models import Atelier  # adapte si besoin

    if request.method == "POST":
        form = SequenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_sequences')
    else:
        form = SequenceForm()

    ateliers = Atelier.objects.all().order_by('nom')
    selected_ateliers = request.POST.getlist('ateliers') if request.method == "POST" else []

    return render(request, "fiches/form_sequence.html", {
        "form": form,
        "ateliers": ateliers,
        "selected_ateliers": [int(a) for a in selected_ateliers],
    })


# Création d'atelier
@login_required
@user_passes_test(is_animateur)
def creer_atelier(request):
    from modules.models import Technique  # Adapte l'import si besoin

    if request.method == "POST":
        form = AtelierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_ateliers')
    else:
        form = AtelierForm()

    # Techniques à passer pour affichage custom
    techniques = Technique.objects.all().order_by('nom')
    # Si tu veux conserver la sélection après erreur :
    selected_techniques = request.POST.getlist('techniques') if request.method == "POST" else []

    return render(request, "fiches/form_atelier.html", {
        "form": form,
        "techniques": techniques,
        "selected_techniques": [int(t) for t in selected_techniques],
    })


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

def get_unique_slug(parent, base_slug):
    slug = base_slug
    i = 1
    # Cherche si le slug existe déjà parmi les enfants du parent
    while parent.get_children().filter(slug=slug).exists():
        slug = f"{base_slug}-{i}"
        i += 1
    return slug

def creer_fiche(request):
    from modules.models import Sequence
    from wagtail.models import Page

    parent_page = Page.objects.get(slug="home")  # À adapter à ta structure

    if request.method == "POST":
        form = FichePageForm(request.POST)
        if form.is_valid():
            fiche = form.save(commit=False)
            # Sécurisation du titre par défaut
            title = form.cleaned_data.get("title") or "Fiche sans titre"
            fiche.title = title
            base_slug = slugify(title)
            fiche.slug = get_unique_slug(parent_page, base_slug)
            parent_page.add_child(instance=fiche)
            fiche.save_revision().publish()
            form.save_m2m()
            return redirect('liste_seances')
    else:
        form = FichePageForm()

    sequences = Sequence.objects.prefetch_related('ateliers__techniques').all().order_by('titre')
    selected_sequences = request.POST.getlist('sequences') if request.method == "POST" else []

    return render(request, "fiches/form_fiche.html", {
        "form": form,
        "sequences": sequences,
        "selected_sequences": [int(s) for s in selected_sequences],
    })