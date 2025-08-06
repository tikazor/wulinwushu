from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages  
from django.shortcuts import render, get_object_or_404, redirect
from fiches.models import FichePage, Sequence, Atelier, Technique
from progression.models import ValidationFiche
from utilisateurs.permissions import can_view_fiche, can_edit_or_delete_fiche, can_edit_or_delete_sequence, can_edit_or_delete_atelier, can_edit_or_delete_technique
from django.core.exceptions import PermissionDenied
from fiches.forms import FichePageForm, SequenceForm, AtelierForm, TechniqueForm




@login_required
def espace_utilisateur(request):
    user = request.user

    # 1️⃣ Toutes les fiches live() (QuerySet)
    qs_live = FichePage.objects.live()

    # 2️⃣ On ne garde que celles que l'utilisateur peut voir
    fiches_publiées = [fiche for fiche in qs_live if can_view_fiche(user, fiche)]

    # 3️⃣ Récupère les IDs des fiches validées
    valid_ids = set(
        ValidationFiche.objects
            .filter(utilisateur=user, valide=True)
            .values_list("fiche_id", flat=True)
    )

    # 4️⃣ Sépare validées et non-validées
    fiches_validées     = [f for f in fiches_publiées if f.id in valid_ids]
    fiches_non_validées = [f for f in fiches_publiées if f.id not in valid_ids]

    # 5️⃣ Calcule le taux de progression
    taux = int(100 * len(fiches_validées) / len(fiches_publiées)) if fiches_publiées else 0

    return render(request, "utilisateurs/espace.html", {
        "fiches_validées":     fiches_validées,
        "fiches_non_validées": fiches_non_validées,
        "taux":                taux,
        "utilisateur":         user,
    })

# ─── Usage pour FichePage ───────────────────────────────────────────────

@login_required
def fiche_detail(request, slug):
    # récupère la FichePage publiée correspondant au slug
    fiche = get_object_or_404(
        FichePage.objects.live().public(),
        slug=slug
    )
    est_validee = fiche.is_validated_by(request.user)
    return render(request, "utilisateurs/fiche_detail.html", {
        "fiche": fiche,
        "est_validee": est_validee,
    })

@login_required
@require_POST
def valider_fiche(request, slug):
    fiche = get_object_or_404(
        FichePage.objects.live().public(),
        slug=slug
    )
    # Vérifier si déjà validée (évite doublons)
    from progression.models import ValidationFiche
    validation, created = ValidationFiche.objects.get_or_create(
        fiche=fiche,
        utilisateur=request.user,
        defaults={"valide": True}
    )
    # Si déjà validée, rien à faire, sinon créée.
    return redirect('fiche_detail', slug=fiche.slug)

@login_required
def supprimer_fiche(request, pk):
    fiche = get_object_or_404(FichePage, pk=pk)
    if not can_edit_or_delete_fiche(request.user, fiche):
        raise PermissionDenied
    if request.method == "POST":
        fiche.delete()
        messages.success(request, "Fiche supprimée avec succès.")
        return redirect("liste_seances")
    return render(request, "fiches/fiche_confirm_delete.html", {"fiche": fiche})

@login_required
def modifier_fiche(request, pk):
    fiche = get_object_or_404(FichePage, pk=pk)
    if not can_edit_or_delete_fiche(request.user, fiche):
        messages.error(request, "Vous n'avez pas le droit de modifier cette fiche.")
        return redirect('liste_seances')
    if request.method == "POST":
        form = FichePageForm(request.POST, instance=fiche)
        if form.is_valid():
            form.save()
            messages.success(request, "Fiche modifiée avec succès.")
            return redirect('detail_seance', pk=fiche.pk)
    else:
        form = FichePageForm(instance=fiche)
    return render(request, "fiches/form_fiche.html", {"form": form, "fiche": fiche})

# ─── FIN de FichePage ────────────────────────────────────────────

# ─── Usage pour sequence ───────────────────────────────────────────────

@login_required
def modifier_sequence(request, pk):
    sequence = get_object_or_404(Sequence, pk=pk)
    if not can_edit_or_delete_sequence(request.user, sequence):
        messages.error(request, "Vous n'avez pas le droit de modifier cette séquence.")
        return redirect('detail_sequence', pk=pk)
    # form handling logique
    if request.method == "POST":
        form = SequenceForm(request.POST, instance=sequence)
        if form.is_valid():
            form.save()
            messages.success(request, "Séquence modifiée avec succès.")
            return redirect('detail_sequence', pk=pk)
    else:
        form = SequenceForm(instance=sequence)
    # Passe la liste ateliers et ateliers cochés
    return render(request, "fiches/form_sequence.html", {"form": form, "sequence": sequence, "ateliers": Atelier.objects.all(), "selected_ateliers": [a.id for a in sequence.ateliers.all()]})

@login_required
def supprimer_sequence(request, pk):
    sequence = get_object_or_404(Sequence, pk=pk)
    if not can_edit_or_delete_sequence(request.user, sequence):
        messages.error(request, "Vous n'avez pas le droit de supprimer cette séquence.")
        return redirect('detail_sequence', pk=pk)
    if request.method == "POST":
        titre = sequence.titre
        sequence.delete()
        messages.success(request, f"La séquence '{titre}' a été supprimée.")
        return redirect('liste_sequences')
    return render(request, "fiches/sequence_confirm_delete.html", {"sequence": sequence})

# ─── Fin de sequence ───────────────────────────────────────────────

# ─── Usage Atelier ───────────────────────────────────────────────
@login_required
def modifier_atelier(request, pk):
    atelier = get_object_or_404(Atelier, pk=pk)
    if not can_edit_or_delete_atelier(request.user, atelier):
        messages.error(request, "Vous n'avez pas le droit de modifier cet atelier.")
        return redirect('detail_atelier', pk=pk)
    if request.method == "POST":
        form = AtelierForm(request.POST, request.FILES, instance=atelier)
        if form.is_valid():
            form.save()
            messages.success(request, "Atelier modifié avec succès.")
            return redirect('detail_atelier', pk=pk)
    else:
        form = AtelierForm(instance=atelier)
    return render(request, "fiches/form_atelier.html", {
        "form": form,
        "atelier": atelier,
        "techniques": Technique.objects.all(),
        "selected_techniques": [t.id for t in atelier.techniques.all()],
    })

@login_required
def supprimer_atelier(request, pk):
    atelier = get_object_or_404(Atelier, pk=pk)
    if not can_edit_or_delete_atelier(request.user, atelier):
        messages.error(request, "Vous n'avez pas le droit de supprimer cet atelier.")
        return redirect('detail_atelier', pk=pk)
    if request.method == "POST":
        nom = atelier.nom
        atelier.delete()
        messages.success(request, f"L'atelier '{nom}' a été supprimé.")
        return redirect('liste_ateliers')
    return render(request, "fiches/atelier_confirm_delete.html", {"atelier": atelier})

# ─── Fin Atelier ───────────────────────────────────────────────

# ─── Usage pour technique ───────────────────────────────────────────────

@login_required
def modifier_technique(request, pk):
    technique = get_object_or_404(Technique, pk=pk)
    if not can_edit_or_delete_technique(request.user, technique):
        messages.error(request, "Vous n'avez pas le droit de modifier cette technique.")
        return redirect('detail_technique', pk=pk)
    if request.method == "POST":
        form = TechniqueForm(request.POST, request.FILES, instance=technique)
        if form.is_valid():
            form.save()
            messages.success(request, "Technique modifiée avec succès.")
            return redirect('detail_technique', pk=pk)
    else:
        form = TechniqueForm(instance=technique)
    return render(request, "fiches/form_technique.html", {
        "form": form,
        "technique": technique,
        # Ajoute d'autres éléments du contexte si nécessaire
    })

@login_required
def supprimer_technique(request, pk):
    technique = get_object_or_404(Technique, pk=pk)
    if not can_edit_or_delete_technique(request.user, technique):
        messages.error(request, "Vous n'avez pas le droit de supprimer cette technique.")
        return redirect('detail_technique', pk=pk)
    if request.method == "POST":
        nom = technique.nom
        technique.delete()
        messages.success(request, f"La technique '{nom}' a été supprimée.")
        return redirect('liste_techniques')
    return render(request, "fiches/technique_confirm_delete.html", {"technique": technique})

# ─── Fin Technique ───────────────────────────────────────────────