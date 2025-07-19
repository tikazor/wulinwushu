from django.shortcuts import render, get_object_or_404
from fiches.models import FichePage, Sequence, Atelier, Technique
from django.db.models import Q

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




def liste_techniques(request):
    q = request.GET.get('q', '').strip()
    techniques = Technique.objects.all()
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
    if q:
        ateliers = ateliers.filter(
            Q(consigne__icontains=q)
            # Ajoute d'autres filtres selon tes champs
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
    ateliers = list(Atelier.objects.all().order_by('pk'))
    current = get_object_or_404(Atelier, pk=pk)
    idx = ateliers.index(current)
    prev_obj = ateliers[idx-1] if idx > 0 else None
    next_obj = ateliers[idx+1] if idx < len(ateliers)-1 else None
    return render(request, "modules/detail_atelier.html", {
        "objet": current,
        "prev_obj": prev_obj,
        "next_obj": next_obj,
        "detail_url": "detail_atelier",  # ou ton nom d’urlpattern
    })

def detail_sequence(request, pk):
    sequences = list(Sequence.objects.all().order_by('pk'))
    current = get_object_or_404(Sequence, pk=pk)
    idx = sequences.index(current)
    prev_obj = sequences[idx-1] if idx > 0 else None
    next_obj = sequences[idx+1] if idx < len(sequences)-1 else None
    return render(request, "modules/detail_sequence.html", {
        "objet": current,
        "prev_obj": prev_obj,
        "next_obj": next_obj,
        "detail_url": "detail_sequence",  # ou ton nom d’urlpattern
    })

def detail_technique(request, pk):
    techniques = list(Technique.objects.all().order_by('pk'))
    current = get_object_or_404(Technique, pk=pk)
    idx = techniques.index(current)
    prev_obj = techniques[idx-1] if idx > 0 else None
    next_obj = techniques[idx+1] if idx < len(techniques)-1 else None
    return render(request, "modules/detail_technique.html", {
        "objet": current,
        "prev_obj": prev_obj,
        "next_obj": next_obj,
        "detail_url": "detail_technique",  # ou ton nom d’urlpattern
    })

def detail_seance(request, pk):
    seances = list(FichePage.objects.all().order_by('pk'))
    current = get_object_or_404(FichePage, pk=pk)
    idx = seances.index(current)
    prev_obj = seances[idx-1] if idx > 0 else None
    next_obj = seances[idx+1] if idx < len(seances)-1 else None
    return render(request, "modules/detail_seance.html", {
        "objet": current,
        "prev_obj": prev_obj,
        "next_obj": next_obj,
        "detail_url": "detail_seance",  # ou ton nom d’urlpattern
    })
