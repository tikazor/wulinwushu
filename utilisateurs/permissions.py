from django.contrib.auth import get_user_model
from fiches.models import FichePage, Sequence, Atelier

User = get_user_model()

def is_animateur(user: User) -> bool:
    """
    Renvoie True si l'utilisateur est authentifié
    et a le rôle 'animateur' dans son Profile.
    """
    profile = getattr(user, "profile", None)
    return bool(user.is_authenticated and profile and profile.role == "animateur")

def can_access_tableau_suivi_global(user: User) -> bool:
    """
    Permission d'accès au tableau de suivi global,
    réservée aux animateurs.
    """
    return is_animateur(user)

def can_view_fiche(user: User, fiche: FichePage) -> bool:
    """
    Une fiche est visible si :
    - elle est publique
    - ou l'utilisateur est animateur
    - ou l'utilisateur est participant
    """
    if fiche.is_public:
        return True
    if fiche.animateurs.filter(id=user.id).exists():
        return True
    if fiche.participants.filter(id=user.id).exists():
        return True
    return False

# ─── Permission pour FichePage ───────────────────────────────────────────────

# def can_edit_fiche(user, fiche: FichePage) -> bool:
#     if user.is_superuser:
#         return True
#     # Animateur uniquement s'il fait partie du M2M
#     return fiche.animateurs.filter(id=user.id).exists()

# def can_delete_fiche(user, fiche: FichePage) -> bool:
#     if user.is_superuser:
#         return True
#     return fiche.animateurs.filter(id=user.id).exists()

def can_edit_or_delete_fiche(user, fiche):
    if user.is_superuser:
        return True
    return user in fiche.animateurs.all()


# ─── Fin FichePage ───────────────────────────────────────────────

def can_view_sequence(user: User, sequence: Sequence) -> bool:
    """
    Une séquence est visible si au moins une fiche qui la contient
    est visible pour l'utilisateur.
    """
    return any(can_view_fiche(user, f) for f in sequence.fichepage_set.all())

def can_view_atelier(user: User, atelier: Atelier) -> bool:
    """
    Un atelier est visible si au moins une séquence qui l'inclut
    est visible pour l'utilisateur.
    """
    return any(can_view_sequence(user, seq) for seq in atelier.sequence_set.all())

def is_public_wubuquan(obj) -> bool:
    """
    Retourne True si l'objet (Atelier ou Technique) est public via le tag 'wubuquan'.
    """
    return obj.tags.filter(name__iexact="wubuquan").exists()