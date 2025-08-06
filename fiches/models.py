import datetime
from django import forms
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from types import SimpleNamespace

# Import Wagtail natif
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.models import Image as WagtailImage
from wagtail.images.models import Image
from wagtail.snippets.models import register_snippet

# Tags & cluster pour vos snippets/taggit
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager



# ─── Technique (snippet) ───────────────────────────────────────────────
@register_snippet
class Technique(models.Model):
    STYLE_CHOICES = [
        ("shaolin", "Shaolin"),
        ("changquan", "Changquan"),
        ("nanquan", "Nanquan"),
        ("autre", "Autre"),
    ]
    ZONE_CHOICES = [
        ("corps entier", "Corps entier"),
        ("main", "Main"),
        ("pied", "Pied"),
        ("autre", "Autre"),
    ]
    CATEGORIE_CHOICES = [
        ("bufa", "Bùfǎ (postures)"),
        ("tuifa", "Tuīfǎ (coups de pied)"),
        ("shoufa", "Shǒufǎ (techniques de main)"),
        ("jibengong", "Jīběngōng (fondamentaux)"),
        ("autre", "Autre"),
    ]

    nom = models.CharField(max_length=100, help_text="Nom romanisé ex: Ma Bu")
    nom_chinois = models.CharField(max_length=50, blank=True, help_text="Idéogramme ou nom en chinois")
    nom_pinyin = models.CharField(max_length=100, blank=True, help_text="Transcription en pinyin ex: Mǎ bù")
    traduction = models.CharField(max_length=200, blank=True, help_text="Traduction littérale ou simplifiée")
    description = models.TextField(blank=True, help_text="Brève description ou usage pédagogique")

    style = models.CharField(max_length=50, choices=STYLE_CHOICES, default="autre")
   
    references = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='referenced_by',
        help_text="Techniques associées ou similaires"
    )

    zone = models.CharField(max_length=50, choices=ZONE_CHOICES, default="corps entier")
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES, default="autre")


    upload_image = models.ImageField(
            "Téléverser une image",
            upload_to="techniques/",
            blank=True,
            null=True,
        )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    video = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    video_embed = models.URLField(blank=True, help_text="Lien vers une vidéo YouTube ou Vimeo")
    lien = models.URLField(blank=True, help_text="Lien complémentaire vers un article, etc.")

    panels = [
        FieldPanel("nom"),
        FieldPanel("nom_chinois"),
        FieldPanel("nom_pinyin"),
        FieldPanel("traduction"),
        FieldPanel("description"),
        FieldPanel("style"),
        FieldPanel("references"), 
        FieldPanel("zone"),
        FieldPanel("categorie"),
        FieldPanel('image'),
        FieldPanel("video"),
        FieldPanel("video_embed"),
        FieldPanel("lien"),
    ]

    def __str__(self) -> str:
        return f"{self.nom} ({self.categorie})"


# ─── ATELIER (snippet) ────────────────────────────────────────────────
@register_snippet
class Atelier(models.Model):
    nom = models.CharField(max_length=100, help_text="titre atelier ex: wubuquan, exercice souplesse")
    techniques = models.ManyToManyField("Technique", blank=True)
    duree = models.PositiveIntegerField(help_text="Durée en minutes")
    series = models.PositiveIntegerField("Nombre de séries", blank=True, null=True, help_text="Ex : 3 séries")
    repetitions = models.PositiveIntegerField("Nombre de répétitions", blank=True, null=True, help_text="Ex : 12 répétitions/série")
    materiels = models.ManyToManyField("Materiel", blank=True, related_name="ateliers")
    consigne = models.TextField(blank=True, help_text="Consigne pédagogique")

    upload_image = models.ImageField(
        "Téléverser une image",
        upload_to="ateliers/",
        blank=True,
        null=True,
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    # CHAMPS AJOUTÉS
    

    panels = [
        FieldPanel("nom"),
        FieldPanel("techniques"),
        FieldPanel("duree"),
        FieldPanel("consigne"),
        FieldPanel('image'),
        FieldPanel("series"),
        FieldPanel("repetitions"),
    ]

    def __str__(self):
        styles = ", ".join(sorted({t.style for t in self.techniques.all() if t.style}))
        zones = ", ".join(sorted({t.zone for t in self.techniques.all() if t.zone}))
        categories = ", ".join(sorted({t.categorie for t in self.techniques.all() if t.categorie}))

        parts = [self.nom]
        if styles:
            parts.append(f"Styles: {styles}")
        if zones:
            parts.append(f"Zones: {zones}")
        if categories:
            parts.append(f"Catégories: {categories}")
        return " | ".join(parts)




# ─── Séquence (snippet) ───────────────────────────────────────────────
@register_snippet
class Sequence(models.Model):
    TYPES = [
        ("echauffement", "Échauffement"),
        ("zuhe", "Zuhe"),
        ("souplesse", "Souplesse"),
        ("gongfang", "Gong Fang"),
        ("taolu", "Taolu"),
        ("autre", "Autre"),
    ]

    titre = models.CharField(max_length=200)
    type_sequence = models.CharField(max_length=50, choices=TYPES)
    ateliers = models.ManyToManyField("Atelier", blank=True)

    panels = [
        FieldPanel("titre"),
        FieldPanel("type_sequence"),
        FieldPanel("ateliers"),
    ]

    def duree_totale(self) -> int:
        """Somme des durées des ateliers de la séquence."""
        return sum(a.duree for a in self.ateliers.all() if a.duree)

    def resume(self):
        ateliers_resume = []
        for atelier in self.ateliers.all():
            techniques = ", ".join(sorted([t.nom for t in atelier.techniques.all()]))
            consigne_debut = (atelier.consigne[:40] + "...") if atelier.consigne and len(atelier.consigne) > 40 else (atelier.consigne or "")
            atelier_info = atelier.nom
            if techniques:
                atelier_info += f" | Techniques: {techniques}"
            if atelier.duree:
                atelier_info += f" | Durée: {atelier.duree} min"
            if consigne_debut:
                atelier_info += f" | Consigne: {consigne_debut}"
            ateliers_resume.append(atelier_info)
        return ateliers_resume

    def __str__(self):
        ateliers_info = "; ".join(self.resume())
        return f"{self.titre} ({self.get_type_sequence_display()}) | Ateliers: {ateliers_info if ateliers_info else 'Aucun'}"



# ─── FichePage ────────────────────────────────────────────────────────
class FichePage(Page):
    # Champs effectifs
    date = models.DateField("Date de la séance", blank=True, null=True)
    niveau = models.CharField(
        max_length=10,
        choices=[
            ("enfant", "Enfant"),
            ("adulte", "Adulte"),
            ("mixte", "Mixte"),
        ],
        default="enfant",
        help_text="Public cible"
    )
    animateurs = models.ManyToManyField(
        User,
        related_name="fiches_animateur",
        blank=True
    )
    participants = models.ManyToManyField(
        User,
        related_name="fiches_participées",
        blank=True
    )
    categories = ClusterTaggableManager(
        through="FichePageTag",
        blank=True
    )
    sequences = models.ManyToManyField(
        Sequence,
        blank=True
    )
    is_public = models.BooleanField(
        default=False,
        help_text="Rendre la fiche visible à tous (ex: Wubuquan)"
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("niveau"),
        FieldPanel("animateurs"),
        FieldPanel("participants"),   # <--- À PLAT
        FieldPanel("is_public"),
        FieldPanel("sequences"),      # <--- À PLAT
        InlinePanel("tagged_items", label="Catégories"),
    ]

    # fiche_info_panels = MultiFieldPanel([
    #     FieldPanel("date"),
    #     FieldPanel("niveau"),
    #     FieldPanel("animateurs"),
    #     FieldPanel("participants"),
    #     FieldPanel("is_public"),
    # ], heading="Informations de la séance")

    # content_panels = Page.content_panels + [
    #     fiche_info_panels,
    #     FieldPanel("participants"),
    #     FieldPanel("sequences"),
    #     InlinePanel("tagged_items", label="Catégories"),
    # ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []
    template = "fiches/fiche_page.html"

    def resume(self):
        ateliers_resume = []
        for atelier in self.ateliers.all():
            techniques = ", ".join(sorted([t.nom for t in atelier.techniques.all()]))
            consigne_debut = (atelier.consigne[:40] + "...") if atelier.consigne and len(atelier.consigne) > 40 else (atelier.consigne or "")
            atelier_info = atelier.nom
            if techniques:
                atelier_info += f" | Techniques: {techniques}"
            if atelier.duree:
                atelier_info += f" | Durée: {atelier.duree} min"
            if consigne_debut:
                atelier_info += f" | Consigne: {consigne_debut}"
            ateliers_resume.append(atelier_info)
        return ateliers_resume




# ─── Tag pour FichePage ───────────────────────────────────────────────
class FichePageTag(TaggedItemBase):
    content_object = ParentalKey(
        "FichePage",
        related_name="tagged_items",
        on_delete=models.CASCADE
    )

@register_snippet
class Materiel(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom