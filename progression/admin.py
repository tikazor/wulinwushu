from django.contrib import admin
from .models import ValidationFiche

@admin.register(ValidationFiche)
class ValidationFicheAdmin(admin.ModelAdmin):
    list_display = ("fiche", "utilisateur", "valide", "date_validation")
    list_filter = ("valide", "date_validation")
