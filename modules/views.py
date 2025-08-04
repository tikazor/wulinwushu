from django.shortcuts import render, get_object_or_404
from fiches.models import FichePage, Sequence, Atelier, Technique
from django.db.models import Q
from utilisateurs.permissions import is_public_wubuquan
from collections import Counter


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




from utilisateurs.permissions import is_public_wubuquan

def liste_techniques(request):
    q = request.GET.get('q', '').strip()
    techniques = Technique.objects.all()

    # Si utilisateur non connecté → filtrer sur tag 'wubuquan'
    if not request.user.is_authenticated:
        techniques = techniques.filter(tags__name__iexact="wubuquan")

    if q:
        techniques = techniques.filter(
            Q(nom__icontains=q) |
            Q(traduction__icontains=q) |
            Q(description__icontains=q) |
            Q(nom_chinois__icontains=q) |
            Q(nom_pinyin__icontains=q)
        )

    return render(request, "modules/liste_techniques.html", {"techniques": techniques, "q": q})


def liste_sequences(request):
    q = request.GET.get('q', '').strip()
    sequences = Sequence.objects.all()
    if q:
        sequences = sequences.filter(
            Q(titre__icontains=q) |
            Q(type_sequence__icontains=q)
        )
    return render(request, "modules/liste_sequences.html", {"sequences": sequences, "q": q})

def liste_ateliers(request):
    q = request.GET.get('q', '').strip()
    ateliers = Atelier.objects.all()

    if not request.user.is_authenticated:
        ateliers = ateliers.filter(tags__name__iexact="wubuquan")

    if q:
        ateliers = ateliers.filter(
            Q(consigne__icontains=q)
        )

    return render(request, "modules/liste_ateliers.html", {"ateliers": ateliers, "q": q})


def liste_seances(request):
    q = request.GET.get('q', '').strip()
    fiches = FichePage.objects.live().public()
    if q:
        fiches = fiches.filter(
            Q(title__icontains=q) |
            Q(participants__icontains=q)
            # Ajoute d'autres champs si besoin
        )
    return render(request, "modules/liste_seances.html", {"fiches": fiches, "q": q})

def detail_atelier(request, pk):
    current = get_object_or_404(Atelier, pk=pk)

    if not request.user.is_authenticated and not is_public_wubuquan(current):
        return render(request, "403.html", status=403)

    ateliers = list(Atelier.objects.all().order_by('pk'))
    idx = ateliers.index(current)
    prev_obj = ateliers[idx-1] if idx > 0 else None
    next_obj = ateliers[idx+1] if idx < len(ateliers)-1 else None
    return render(request, "modules/detail_atelier.html", {
        "objet": current,
        "prev_obj": prev_obj,
        "next_obj": next_obj,
        "detail_url": "detail_atelier",
    })


def detail_sequence(request, pk):
    sequences = list(Sequence.objects.all().order_by('pk'))
    current = get_object_or_404(Sequence, pk=pk)
    idx = sequences.index(current)
    prev_obj = sequences[idx-1] if idx > 0 else None
    next_obj = sequences[idx+1] if idx < len(sequences)-1 else None

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
    return render(request, "modules/detail_technique.html", {
        "objet": current,
        "prev_obj": prev_obj,
        "next_obj": next_obj,
        "detail_url": "detail_technique",
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

