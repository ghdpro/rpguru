"""RPGuru Library forms"""

from django import forms

from changerequest.forms import HistoryCommentOptionalMixin

from .models import Platform


class PlatformCreateForm(HistoryCommentOptionalMixin, forms.ModelForm):

    class Meta:
        model = Platform
        fields = ['name', 'slug', 'short', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class PlatformUpdateForm(PlatformCreateForm):
    pass
