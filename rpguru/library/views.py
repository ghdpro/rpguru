"""RPGuru Library views"""

from django import forms
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView

from changerequest.views import PermissionMessageMixin, HistoryFormViewMixin, HistoryFormsetViewMixin, \
    ListQueryStringMixin
from artwork.views import ArtworkActiveMixin

from .forms import AttributeForm
from .models import Game


class AttributeMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set Permission Required dynamically based on Model name
        self.permission_required += self.model._meta.model_name
        # Inject Model into ModelForm
        self.form_class = forms.models.modelform_factory(self.model, self.form_class)

    def get_success_url(self):
        # Generate success URL dynamically based on Model name
        return self.object.get_absolute_url(self.model._meta.model_name + ':update')


class AttributeCreateView(PermissionMessageMixin, HistoryFormViewMixin, AttributeMixin, CreateView):
    permission_required = 'library.add_'
    template_name = 'library/create.html'
    form_class = AttributeForm


class AttributeUpdateView(PermissionMessageMixin, HistoryFormViewMixin, AttributeMixin, UpdateView):
    permission_required = 'library.change_'
    template_name = 'library/update.html'
    form_class = AttributeForm


class AttributeListView(PermissionMessageMixin, ListQueryStringMixin, ListView):
    permission_required = 'library.change_'
    template_name = 'library/list.html'
    paginate_by = 25
    ALLOWED_ORDER = {
        'DEFAULT': ['name'],  # Also equivalent to 'name'
        '-name': ['-name']
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set Permission Required dynamically based on Model name
        self.permission_required += self.model._meta.model_name

    def get_absolute_url(self):
        return reverse(self.model._meta.model_name + ':browse')


class AttributeDetailView(DetailView):
    template_name = 'library/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games'] = Game.cat.filter(**{self.model._meta.model_name: context['object']})
        return context


class AttributeArtworkView(PermissionMessageMixin, ArtworkActiveMixin, HistoryFormsetViewMixin, UpdateView):
    permission_required = 'library.change_'
    template_name = 'library/artwork.html'
    artwork = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set Permission Required dynamically based on Model name
        self.permission_required += self.model._meta.model_name
        # Create form using Artwork Model
        self.form_class = forms.models.modelform_factory(self.artwork, fields=['image'])
        # Create formset
        self.formset_class = forms.models.inlineformset_factory(self.model, self.artwork, form=self.form_class,
                                                                extra=1, can_delete=True)

    def get_success_url(self):
        # Generate success URL dynamically based on Model name
        return self.object.get_absolute_url(self.model._meta.model_name + ':artwork')


class FrontpageView(TemplateView):
    template_name = 'frontpage.html'
