from django.shortcuts import render, get_object_or_404
from fiches.models import FichePage, Sequence, Atelier, Technique
from django.db.models import Q
from utilisateurs.permissions import can_edit_or_delete_sequence, is_public_wubuquan, can_edit_or_delete_atelier,can_edit_or_delete_technique
from collections import Counter
import unicodedata

def normalize(s):
    if not s:
        return ""
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    ).lower()


def liste_modules(request):
    fiches = FichePage.objects.live().public()
    print("FICHES :", list(fiches))
    for f in fiches:
        print(f, "slug=", getattr(f, "slug", None), "url=", getattr(f, "url", None))
    context = {
        "fiches": fiches,
        "sequences": Sequence.objects.all(),
        "ateliers": Atelier.objects.all(),
        "techniques": Technique.objects.all(),
    }
    return render(request, "modules/liste.html", context)


from .models import Technique

def liste_techniques(request):
    q = request.GET.get('q', '').strip()
    style = request.GET.get('style', '')
    zone = request.GET.get('zone', '')
    categorie = request.GET.get('categorie', '')

    techniques = Technique.objects.all()

    if not request.user.is_authenticated:
        techniques = techniques.filter(tags__name__iexact="wubuquan")

    if style:
        techniques = techniques.filter(style=style)
    if zone:
        techniques = techniques.filter(zone=zone)
    if categorie:
        techniques = techniques.filter(categorie=categorie)

    # ==== Dernier filtre accent-insensitive, on passe en liste ====
    model_fields = [f.name for f in Technique._meta.get_fields() if f.get_internal_type() in ['CharField', 'TextField']]

    if q:
        q_norm = normalize(q)
        techniques = [
            t for t in techniques
            if any(
                q_norm in normalize(getattr(t, field) or '')
                for field in model_fields
            )
        ]

    # Ne PAS refaire .filter() ou .distinct() après ce passage en liste !
    # Si tu dois passer à la liste plus tard (ex: pagination), fais-le vraiment en dernier

    styles = Technique.objects.values_list('style', flat=True).distinct().order_by('style')
    zones = Technique.objects.values_list('zone', flat=True).distinct().order_by('zone')
    categories = Technique.objects.values_list('categorie', flat=True).distinct().order_by('categorie')

    return render(request, "modules/liste_techniques.html", {
        "techniques": techniques,  # <--- C'est déjà une liste, PAS de .distinct()
        "q": q,
        "selected_style": style,
        "selected_zone": zone,
        "selected_categorie": categorie,
        "styles": styles,
        "zones": zones,
        "categories": categories,
    })


def liste_sequences(request):
    q = request.GET.get('q', '').strip()
    type_sequence = request.GET.get('type_sequence', '')
    style = request.GET.get('style', '')
    zone = request.GET.get('zone', '')
    categorie = request.GET.get('categorie', '')

    sequences = Sequence.objects.all()

    if type_sequence:
        sequences = sequences.filter(type_sequence=type_sequence)
    if style:
        sequences = sequences.filter(ateliers__techniques__style=style)
    if zone:
        sequences = sequences.filter(ateliers__techniques__zone=zone)
    if categorie:
        sequences = sequences.filter(ateliers__techniques__categorie=categorie)

    # Accent-insensitive EN DERNIER
    model_fields = [f.name for f in Sequence._meta.get_fields() if f.get_internal_type() in ['CharField', 'TextField']]

    if q:
        q_norm = normalize(q)
        sequences = [
            s for s in sequences
            if any(
                q_norm in normalize(getattr(s, field) or '')
                for field in model_fields
            )
        ]


    # Pas de .distinct() ni de .filter() après ce passage en liste !
    types_sequences = Sequence.objects.values_list('type_sequence', flat=True).distinct().order_by('type_sequence')
    styles = Technique.objects.values_list('style', flat=True).distinct().order_by('style')
    zones = Technique.objects.values_list('zone', flat=True).distinct().order_by('zone')
    categories = Technique.objects.values_list('categorie', flat=True).distinct().order_by('categorie')

    types_sequences = [t for t in types_sequences if t]
    styles = [s for s in styles if s]
    zones = [z for z in zones if z]
    categories = [c for c in categories if c]

    return render(request, "modules/liste_sequences.html", {
        "sequences": sequences,
        "q": q,
        "selected_type_sequence": type_sequence,
        "selected_style": style,
        "selected_zone": zone,
        "selected_categorie": categorie,
        "types_sequences": types_sequences,
        "styles": styles,
        "zones": zones,
        "categories": categories,
    })






def liste_seances(request):
    q = request.GET.get('q', '').strip()
    animateur_id = request.GET.get('animateur', '')
    participant_id = request.GET.get('participant', '')
    style = request.GET.get('style', '')
    zone = request.GET.get('zone', '')
    categorie = request.GET.get('categorie', '')

    fiches = FichePage.objects.live().public()

    if animateur_id:
        fiches = fiches.filter(animateurs__id=animateur_id)
    if participant_id:
        fiches = fiches.filter(participants__id=participant_id)
    if style:
        fiches = fiches.filter(sequences__ateliers__techniques__style=style)
    if zone:
        fiches = fiches.filter(sequences__ateliers__techniques__zone=zone)
    if categorie:
        fiches = fiches.filter(sequences__ateliers__techniques__categorie=categorie)

    # Accent-insensitive EN DERNIER
    model_fields = [f.name for f in FichePage._meta.get_fields() if f.get_internal_type() in ['CharField', 'TextField']]

    if q:
        q_norm = normalize(q)
        fiches = [
            f for f in fiches
            if any(
                q_norm in normalize(getattr(f, field) or '')
                for field in model_fields
            )
        ]


    animateurs = (
        FichePage.objects.live().public()
        .values_list('animateurs__id', 'animateurs__first_name', 'animateurs__last_name')
        .distinct().order_by('animateurs__last_name', 'animateurs__first_name')
    )
    participants = (
        FichePage.objects.live().public()
        .values_list('participants__id', 'participants__first_name', 'participants__last_name')
        .distinct().order_by('participants__last_name', 'participants__first_name')
    )

    styles = Technique.objects.values_list('style', flat=True).distinct().order_by('style')
    zones = Technique.objects.values_list('zone', flat=True).distinct().order_by('zone')
    categories = Technique.objects.values_list('categorie', flat=True).distinct().order_by('categorie')

    styles = [s for s in styles if s]
    zones = [z for z in zones if z]
    categories = [c for c in categories if c]

    animateurs_list = [
        {'id': a[0], 'nom': f"{a[2].upper()} {a[1]}"}
        for a in animateurs if a[0]
    ]
    participants_list = [
        {'id': p[0], 'nom': f"{p[2].upper()} {p[1]}"}
        for p in participants if p[0]
    ]

    return render(request, "modules/liste_seances.html", {
        "fiches": fiches,
        "q": q,
        "selected_animateur": animateur_id,
        "selected_participant": participant_id,
        "selected_style": style,
        "selected_zone": zone,
        "selected_categorie": categorie,
        "animateurs": animateurs_list,
        "participants": participants_list,
        "styles": styles,
        "zones": zones,
        "categories": categories,
    })

# ─── Modules ATELIER  ────────────────────────────────────────────────
def detail_atelier(request, pk):
    current = get_object_or_404(Atelier, pk=pk)

    if not request.user.is_authenticated and not is_public_wubuquan(current):
        return render(request, "403.html", status=403)

    ateliers = list(Atelier.objects.all().order_by('pk'))
    idx = ateliers.index(current)
    prev_obj = ateliers[idx-1] if idx > 0 else None
    next_obj = ateliers[idx+1] if idx < len(ateliers)-1 else None
    can_edit = can_edit_or_delete_atelier(request.user, object)

    return render(request, "modules/detail_atelier.html", {
        "objet": current,
        "prev_obj": prev_obj,
        "next_obj": next_obj,
        "detail_url": "detail_atelier",
        "can_edit_atelier": can_edit,
    })

def liste_ateliers(request):
    q = request.GET.get('q', '').strip()
    style = request.GET.get('style', '')
    zone = request.GET.get('zone', '')
    categorie = request.GET.get('categorie', '')

    ateliers = Atelier.objects.all()

    if not request.user.is_authenticated:
        ateliers = ateliers.filter(tags__name__iexact="wubuquan")

    if style:
        ateliers = ateliers.filter(techniques__style=style)
    if zone:
        ateliers = ateliers.filter(techniques__zone=zone)
    if categorie:
        ateliers = ateliers.filter(techniques__categorie=categorie)

    # Accent-insensitive filter EN DERNIER
    model_fields = [
        f.name for f in Atelier._meta.get_fields()
        if f.get_internal_type() in ['CharField', 'TextField']
    ]
    if q:
        q_norm = normalize(q)
        ateliers = [
            a for a in ateliers
            if any(
                q_norm in normalize(getattr(a, field) or '')
                for field in model_fields
            )
        ]

    # Ne PAS faire .distinct() après !
    styles = Technique.objects.values_list('style', flat=True).distinct().order_by('style')
    zones = Technique.objects.values_list('zone', flat=True).distinct().order_by('zone')
    categories = Technique.objects.values_list('categorie', flat=True).distinct().order_by('categorie')

    return render(request, "modules/liste_ateliers.html", {
        "ateliers": ateliers,  # <--- PAS de .distinct() ici
        "q": q,
        "selected_style": style,
        "selected_zone": zone,
        "selected_categorie": categorie,
        "styles": styles,
        "zones": zones,
        "categories": categories,
    })

# ─── Fin ATELIER  ────────────────────────────────────────────────


def detail_sequence(request, pk):
    sequences = list(Sequence.objects.all().order_by('pk'))
    current = get_object_or_404(Sequence, pk=pk)
    idx = sequences.index(current)
    prev_obj = sequences[idx-1] if idx > 0 else None
    next_obj = sequences[idx+1] if idx < len(sequences)-1 else None
    can_edit = can_edit_or_delete_sequence(request.user, current)
    
    # Extraire toutes les techniques de tous les ateliers de la séquence
    all_techs = []
    for at in current.ateliers.all():
        all_techs.extend(list(at.techniques.all()))
    # Compter occurrences
    tech_counts = Counter(all_techs)
    # Liste unique des techniques (pour affichage)
    unique_techs = list(tech_counts.keys())

    return render(request, "modules/detail_sequence.html", {
        "objet": current,
        "prev_obj": prev_obj,
        "next_obj": next_obj,
        "detail_url": "detail_sequence",
        "can_edit_sequence": can_edit,
        "unique_techs": unique_techs,
        "tech_counts": tech_counts,
    })

def detail_technique(request, pk):
    current = get_object_or_404(Technique, pk=pk)

    if not request.user.is_authenticated and not is_public_wubuquan(current):
        return render(request, "403.html", status=403)

    techniques = list(Technique.objects.all().order_by('pk'))
    idx = techniques.index(current)
    prev_obj = techniques[idx-1] if idx > 0 else None
    next_obj = techniques[idx+1] if idx < len(techniques)-1 else None
    can_edit = can_edit_or_delete_technique(request.user, object)
    return render(request, "modules/detail_technique.html", {
        "objet": current,
        "prev_obj": prev_obj,
        "next_obj": next_obj,
        "detail_url": "detail_technique",
        "can_edit_technique": can_edit,
    })




def detail_seance(request, pk):
    seances = list(FichePage.objects.all().order_by('pk'))
    current = get_object_or_404(FichePage, pk=pk)
    idx = seances.index(current)
    prev_obj = seances[idx-1] if idx > 0 else None
    next_obj = seances[idx+1] if idx < len(seances)-1 else None

    print("Séance :", current)
    print("Séquences :", list(current.sequences.all()))
    for seq in current.sequences.all():
        print(" - Sequence:", seq, "Ateliers:", list(seq.ateliers.all()))
        for at in seq.ateliers.all():
            print("   - Atelier:", at, "Techniques:", list(at.techniques.all()))
    print("Participants :", list(current.participants.all()))

    # Séquences
    all_sequences = list(current.sequences.all())

    # Ateliers (depuis chaque séquence)
    all_ateliers = []
    for seq in all_sequences:
        all_ateliers.extend(list(seq.ateliers.all()))
    unique_ateliers = list(dict.fromkeys(all_ateliers))  # conserve l'ordre, unique

    # Techniques (depuis chaque atelier de toutes les séquences)
    all_techs = []
    for at in unique_ateliers:
        all_techs.extend(list(at.techniques.all()))
    tech_counts = Counter(all_techs)
    unique_techs = list(tech_counts.keys())

    return render(request, "modules/detail_seance.html", {
        "objet": current,
        "prev_obj": prev_obj,
        "next_obj": next_obj,
        "detail_url": "detail_seance",
        "all_sequences": all_sequences,
        "unique_ateliers": unique_ateliers,
        "unique_techs": unique_techs,
        "tech_counts": tech_counts,
    })

