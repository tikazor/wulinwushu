from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User
from .models import Profile

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('pratiquant', 'Pratiquant'),
        ('animateur', 'Animateur'),
        ('admin', 'Admin'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Rôle")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role")



class SignupForm(UserCreationForm):
    ROLE_CHOICES = Profile.ROLE_CHOICES
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Rôle")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role")

    def save(self, commit=True):
        user = super().save(commit)
        user.profile.role = self.cleaned_data["role"]
        if commit:
            user.profile.save()
        return user
