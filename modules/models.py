# modules/models.py

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField

from fiches.models import FichePage, Sequence, Atelier, Technique

class ModuleIndexPage(Page):
    """Regroupe tout le contenu pédagogique par catégories."""
    subpage_types = []               # pas d'enfants Wagtail ici
    parent_page_types = ["home.HomePage"]

    def get_context(self, request):
        context = super().get_context(request)

        # 🔖 Séances (fiches) triées par date décroissante
        context["fiches"] = FichePage.objects.live().order_by("-date")

        # 🗂️ Séquences triées par titre
        context["sequences"] = Sequence.objects.all().order_by("titre")

        # 🔧 Ateliers triés par durée croissante
        context["ateliers"] = Atelier.objects.all().order_by("duree")

        # 🥋 Techniques triées par style puis nom
        context["techniques"] = Technique.objects.all().order_by("nom_pinyin", "description")

        return context

class ModulePage(Page):
    """Page détaillée d’un module (optionnelle)."""
    description = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]
