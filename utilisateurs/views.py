from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.shortcuts import render, get_object_or_404, redirect
from fiches.models import FichePage
from progression.models import ValidationFiche
from utilisateurs.permissions import can_view_fiche


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

