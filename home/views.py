from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login

from fiches.models import FichePage
from progression.models import ValidationFiche
from utilisateurs.forms import SignupForm




def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("espace_utilisateur")
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})

def accueil(request):
    return render(request, "home/accueil.html")


