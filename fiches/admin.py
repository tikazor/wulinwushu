from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Technique, Atelier, Sequence, FichePage

@admin.register(Atelier)
class AtelierAdmin(admin.ModelAdmin):
    list_display = ("__str__", "duree", "techniques_list")

    def techniques_list(self, obj):
        return ", ".join(t.nom for t in obj.techniques.all())
    techniques_list.short_description = "Techniques associées"

admin.site.register(Sequence)

@admin.register(Technique)
class TechniqueAdmin(ImportExportModelAdmin):
    pass

@admin.register(FichePage)
class FichePageAdmin(admin.ModelAdmin):
    filter_horizontal = ('participants', 'sequences',)
