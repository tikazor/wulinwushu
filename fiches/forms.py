# fiches/forms.py
from django import forms
from wagtail.fields import StreamField
from .models import FichePage, Sequence, Atelier, Technique
from .blocks import SequenceBlock, SequenceChooserBlock

class FichePageForm(forms.ModelForm):
    class Meta:
        model = FichePage
        fields = ['title', 'date', 'niveau', 'animateurs', 'participants', 'sequences']
        widgets = {
            'sequences': forms.SelectMultiple(attrs={"size": 8, "class": "w-full rounded"})
        }

class SequenceForm(forms.ModelForm):
    class Meta:
        model = Sequence
        fields = ['titre', 'type_sequence', 'ateliers']

class AtelierForm(forms.ModelForm):
    class Meta:
        model = Atelier
        fields = ['techniques', 'duree', 'consigne']

class TechniqueForm(forms.ModelForm):
    class Meta:
        model = Technique
        fields = ['nom', 'nom_chinois', 'nom_pinyin', 'traduction', 'description',
                  'style', 'zone', 'categorie', 'image', 'video', 'video_embed', 'lien']
