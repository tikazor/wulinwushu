from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Technique, Atelier, Sequence, FichePage

# ----------------------------------------
@admin.register(Atelier)
class AtelierAdmin(ImportExportModelAdmin):
    list_display = ("__str__", "duree", "techniques_list")
    filter_horizontal = ('techniques',)

    class Media:
        js = ('admin/js/filter_horizontal_accent_insensitive.js',)



    def techniques_list(self, obj):
        return ", ".join(t.nom for t in obj.techniques.all())
    techniques_list.short_description = "Techniques associées"
# ----------------------------------------

@admin.register(Sequence)
class SequenceAdmin(admin.ModelAdmin):
    filter_horizontal = ('ateliers',)  # Dual-list ateliers dans séquence

@admin.register(Technique)
class TechniqueAdmin(ImportExportModelAdmin):
    pass

@admin.register(FichePage)
class FichePageAdmin(admin.ModelAdmin):
    filter_horizontal = ('participants', 'sequences',)  # Dual-list séquences dans séance
