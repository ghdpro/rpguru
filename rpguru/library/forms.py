"""RPGuru Library forms"""

from django import forms

from changerequest.forms import HistoryCommentOptionalForm

from .models import Game, GameArtwork


class AttributeForm(HistoryCommentOptionalForm, forms.ModelForm):

    class Meta:
        fields = ['name', 'slug', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class PlatformForm(HistoryCommentOptionalForm, forms.ModelForm):

    class Meta:
        fields = ['name', 'slug', 'short', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class GameForm(HistoryCommentOptionalForm, forms.ModelForm):

    class Meta:
        model = Game
        fields = ['title', 'jp_date', 'na_date', 'eu_date', 'audio', 'franchise_main', 'franchise_side', 'platform',
                  'developer', 'publisher', 'genre', 'verdict', 'description']
        widgets = {
            'audio': forms.SelectMultiple(attrs={'size': 5}),
            'platform': forms.SelectMultiple(attrs={'size': 5}),
            'developer': forms.SelectMultiple(attrs={'size': 5}),
            'publisher': forms.SelectMultiple(attrs={'size': 5}),
            'genre': forms.SelectMultiple(attrs={'size': 5}),
            'description': forms.Textarea(attrs={'rows': 4})
        }


GameArtworkForm = forms.models.modelform_factory(GameArtwork, fields=['image'])
GameArtworkFormset = forms.models.inlineformset_factory(Game, GameArtwork, form=GameArtworkForm,
                                                        extra=1, can_delete=True)
