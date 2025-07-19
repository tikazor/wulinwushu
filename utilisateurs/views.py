from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.shortcuts import render, get_object_or_404, redirect
from fiches.models import FichePage
from progression.models import ValidationFiche

@login_required
def espace_utilisateur(request):
    utilisateur = request.user

    # Toutes les fiches publiées
    fiches_publiées = FichePage.objects.live().public()

    # Fiches validées par l'utilisateur
    fiches_validées_ids = ValidationFiche.objects.filter(
        utilisateur=utilisateur,
        valide=True
    ).values_list("fiche__id", flat=True)

    # Fiches non validées
    fiches_non_validées = fiches_publiées.exclude(id__in=fiches_validées_ids)
    fiches_validées = fiches_publiées.filter(id__in=fiches_validées_ids)

    return render(request, "utilisateurs/espace.html", {
        "fiches_validées": fiches_validées,
        "fiches_non_validées": fiches_non_validées,
        "utilisateur": utilisateur,
    })

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

