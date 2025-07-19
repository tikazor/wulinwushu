from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login

from fiches.models import FichePage
from progression.models import ValidationFiche
from utilisateurs.forms import CustomUserCreationForm




def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("espace_utilisateur")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


