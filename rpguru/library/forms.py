"""RPGuru Library forms"""

from django import forms

from changerequest.forms import HistoryCommentOptionalForm

from .models import Platform, PlatformArtwork


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
