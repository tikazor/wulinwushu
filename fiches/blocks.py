from wagtail import blocks
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock

#from .models import Atelier, Sequence


# Liste des types (dupliquez models.Sequence.TYPES ici)
TYPE_SEQUENCE_CHOICES = [
    ("echauffement", "Échauffement"),
    ("zuhe", "Zuhe"),
    ("souplesse", "Souplesse"),
    ("gongfang", "Gong Fang"),
    ("taolu", "Taolu"),
    ("autre", "Autre"),
]

class AtelierBlock(blocks.StructBlock):
    techniques = blocks.ListBlock(SnippetChooserBlock('fiches.Technique'),help_text="Ajouter une ou plusieurs techniques")
    duree = blocks.IntegerBlock(required=True, help_text="Durée de l'atelier (en minutes)")
    consigne = blocks.RichTextBlock(required=False, help_text="Consigne pédagogique ou déroulé de l'atelier")
    illustration = ImageChooserBlock(required=False, help_text="Image ou schéma d'appui (facultatif)")

    class Meta:
        template = "blocks/atelier_block.html"
        icon = "form"
        label = "Nouvel Atelier"

class AtelierChooserBlock(blocks.StructBlock):
    # pour réutiliser un atelier pré-enregistré
    atelier = SnippetChooserBlock("fiches.Atelier", label="Atelier existant")

    class Meta:
        template = "blocks/atelier_chooser_block.html"
        icon = "snippet"
        label = "Atelier pré-enregistré"

class SequenceBlock(blocks.StructBlock):
    titre = blocks.CharBlock(required=True, help_text="Titre de la séquence, ex: Échauffement")
    type_sequence = blocks.ChoiceBlock(choices= TYPE_SEQUENCE_CHOICES, help_text="Type de séquence pour classement pédagogique")
    ateliers = blocks.StreamBlock([
        ("new_atelier", AtelierBlock()),
        ("choose_atelier", AtelierChooserBlock()),
    ], help_text="Ajouter un ou plusieurs ateliers (neuf ou pré-enregistré)", min_num=1)

    class Meta:
        template = "blocks/sequence_block.html"
        icon = "folder-open-inverse"
        label = "Séquence (nouvelle)"

class SequenceChooserBlock(blocks.StructBlock):
    sequence = SnippetChooserBlock("fiches.Sequence", label="Séquence existante")

    class Meta:
        template = "blocks/sequence_chooser_block.html"
        icon = "snippet"
        label = "Séquence pré-enregistrée"
