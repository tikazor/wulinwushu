from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import Technique, Atelier, Sequence

# ----------------------------
# Technique
# ----------------------------
class TechniqueAdmin(ModelAdmin):
    model = Technique
    menu_label = "Techniques"
    menu_icon = "list-ul"
    list_display = ("nom", "style", "zone")
    search_fields = ("nom", "style", "zone")

modeladmin_register(TechniqueAdmin)

# ----------------------------
# Atelier
# ----------------------------
class AtelierAdmin(ModelAdmin):
    model = Atelier
    menu_label = "Ateliers"
    menu_icon = "form"
list_display = ("__str__", "duree", "techniques_list")
search_fields = ("technique__nom", "consigne")

def techniques_list(self, obj):
    return ", ".join(t.nom for t in obj.techniques.all())


modeladmin_register(AtelierAdmin)

# ----------------------------
# Séquence
# ----------------------------
class SequenceAdmin(ModelAdmin):
    model = Sequence
    menu_label = "Séquences"
    menu_icon = "folder-open-inverse"
    list_display = ("titre", "type_sequence")
    search_fields = ("titre",)

modeladmin_register(SequenceAdmin)
