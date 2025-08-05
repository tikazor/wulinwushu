# fiches/forms.py
from django import forms
from wagtail.fields import StreamField
from .models import FichePage, Sequence, Atelier, Technique
from .blocks import SequenceBlock, SequenceChooserBlock

class FichePageForm(forms.ModelForm):
    class Meta:
        model = FichePage
        # Liste **uniquement** les champs personnalisés que tu veux
        fields = [
            'title','date', 'niveau', 'animateurs', 'participants',
            'is_public', 'sequences', 'categories'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            # Personnalise les autres widgets si besoin
        }
        labels = {
            "title": "Titre de la fiche séance",
        }

class SequenceForm(forms.ModelForm):
    class Meta:
        model = Sequence
        fields = ['titre', 'type_sequence', 'ateliers']

class AtelierForm(forms.ModelForm):
    class Meta:
        model = Atelier
        fields = ['nom','techniques', 'duree', 'series', 'repetitions','materiels', 'consigne']

class TechniqueForm(forms.ModelForm):
    class Meta:
        model = Technique
        fields = ['nom', 'nom_chinois', 'nom_pinyin', 'traduction', 'description',
                  'style','references', 'zone', 'categorie', 'image', 'video', 'video_embed', 'lien']
