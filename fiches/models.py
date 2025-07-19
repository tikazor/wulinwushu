from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from types import SimpleNamespace
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet

from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager

from .blocks import SequenceBlock, SequenceChooserBlock


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
    nom_chinois = models.CharField(max_length=50, blank=True,
                                   help_text="Idéogramme ou nom en chinois")
    nom_pinyin = models.CharField(max_length=100, blank=True,
                                  help_text="Transcription en pinyin ex: Mǎ bù")
    traduction = models.CharField(max_length=200, blank=True,
                                  help_text="Traduction littérale ou simplifiée")
    description = models.TextField(blank=True,
                                   help_text="Brève description ou usage pédagogique")

    style = models.CharField(max_length=50, choices=STYLE_CHOICES, default="autre")
    zone = models.CharField(max_length=50, choices=ZONE_CHOICES,
                            default="corps entier")
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES,
                                 default="autre")

    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )
    video = models.ForeignKey(
        "wagtaildocs.Document", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )
    video_embed = models.URLField(blank=True,
                                  help_text="Lien vers une vidéo YouTube ou Vimeo")
    lien = models.URLField(blank=True,
                           help_text="Lien complémentaire vers un article, etc.")

    panels = [
        FieldPanel("nom"),
        FieldPanel("nom_chinois"),
        FieldPanel("nom_pinyin"),
        FieldPanel("traduction"),
        FieldPanel("description"),
        FieldPanel("style"),
        FieldPanel("zone"),
        FieldPanel("categorie"),
        FieldPanel("image"),
        FieldPanel("video"),
        FieldPanel("video_embed"),
        FieldPanel("lien"),
    ]

    def __str__(self):
        return f"{self.nom} ({self.categorie})"


@register_snippet
class Atelier(models.Model):
    techniques = models.ManyToManyField("Technique", blank=True)
    duree = models.PositiveIntegerField(help_text="Durée en minutes")
    consigne = models.TextField(blank=True, help_text="Consigne pédagogique")

    panels = [
        FieldPanel("techniques"),
        FieldPanel("duree"),
        FieldPanel("consigne"),
    ]

    def __str__(self):
        techs = ", ".join(t.nom for t in self.techniques.all())
        return f"{techs or 'Sans technique'} – {self.duree} min"


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

    def duree_totale(self):
        return sum(a.duree for a in self.ateliers.all())

    def __str__(self):
        return self.titre


class FichePage(Page):
    NIVEAU_CHOICES = [
        ("enfant", "Enfant"),
        ("adulte", "Adulte"),
        ("mixte", "Mixte"),
    ]

    date = models.DateField("Date de la séance", blank=True, null=True)
    niveau = models.CharField(
        max_length=10, choices=NIVEAU_CHOICES, default="enfant",
        help_text="Public cible"
    )
    animateurs = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="fiches_animateur"
    )
    participants = models.TextField(blank=True,
                                    help_text="Liste des participants")

    categories = ClusterTaggableManager(through="FichePageTag", blank=True)

    sequences = models.ManyToManyField(Sequence, blank=True)
    # sequences = StreamField(
    #     [
    #         ("new_sequence", SequenceBlock()),
    #         ("choose_sequence", SequenceChooserBlock()),
    #     ],
    #     use_json_field=True
    # )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("date"),
            FieldPanel("niveau"),
            FieldPanel("animateurs"),
            FieldPanel("participants"),
        ], heading="Infos séance"),
        FieldPanel("sequences"),
        InlinePanel("tagged_items", label="Catégories"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        sequences_data = []
        total_global = 0

        for block in self.sequences:
            titre   = block.value["titre"]
            seqtype = block.value["type_sequence"]

            seq_total   = 0
            ateliers_ds = []

            for at_block in block.value["ateliers"]:
                if at_block.block_type == "choose_atelier":
                    # atelier existant (snippet) → c’est un vrai modèle Atelier
                    atelier_model = at_block.value["atelier"]
                    duree     = atelier_model.duree
                    consigne  = atelier_model.consigne
                    techniques = atelier_model.techniques.all()
                else:
                    # inline AtelierBlock → StructValue
                    sv = at_block.value
                    duree      = sv["duree"]
                    consigne   = sv["consigne"]
                    techniques = sv["techniques"]  # List of Technique instances

                seq_total += duree
                ateliers_ds.append(
                    SimpleNamespace(
                        duree=duree,
                        consigne=consigne,
                        techniques=techniques,
                    )
                )

            total_global += seq_total
            sequences_data.append(
                {
                    "titre": titre,
                    "type": seqtype,
                    "ateliers": ateliers_ds,
                    "dur_total": seq_total,
                }
            )

        context["sequences_data"] = sequences_data
        context["total_duration"] = total_global
        return context

    def is_validated_by(self, user):
        if not user.is_authenticated:
            return False
        return self.validations.filter(utilisateur=user, valide=True).exists()

    @property
    def duree_totale(self):
        total = 0
        for seq_block in self.sequences:
            ateliers = seq_block.value.get("ateliers") or []
            for atelier_block in ateliers:
                if atelier_block.block_type == "choose_atelier":
                    # snippet Atelier (modèle)
                    atelier = atelier_block.value.get("atelier")
                    if atelier:
                        total += atelier.duree
                else:
                    # StructValue pour inline
                    sv = atelier_block.value
                    total += sv.get("duree", 0)
        return total


    # def clean(self):
    #     super().clean()
    #     if not self.date:
    #         raise ValidationError({"date": "La date est obligatoire."})
    #     if not self.sequences:
    #         raise ValidationError({"sequences": "Ajoutez au moins une séquence."})

    parent_page_types = ["home.HomePage"]
    subpage_types = []
    template = "fiches/fiche_page.html"


class FichePageTag(TaggedItemBase):
    content_object = ParentalKey(
        "FichePage", related_name="tagged_items", on_delete=models.CASCADE
    )
    # modules/views.py ou fiches/views.py



