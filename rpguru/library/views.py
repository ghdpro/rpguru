"""RPGuru Library views"""

from django import forms
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView

from changerequest.views import PermissionMessageMixin, HistoryFormViewMixin

from .forms import AttributeForm


class SuccessURLMixin:

    def get_success_url(self):
        return self.object.get_absolute_url(self.model._meta.model_name + ':update')


class AttributeEditMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set Permission Required dynamically based on Model name
        self.permission_required += self.model._meta.model_name
        # Inject Model into ModelForm
        self.form_class = forms.models.modelform_factory(self.model, self.form_class)


class AttributeCreateView(PermissionMessageMixin, HistoryFormViewMixin, SuccessURLMixin,
                          AttributeEditMixin, CreateView):
    permission_required = 'library.add_'
    template_name = 'library/create.html'
    form_class = AttributeForm


class AttributeUpdateView(PermissionMessageMixin, HistoryFormViewMixin, SuccessURLMixin,
                          AttributeEditMixin, UpdateView):
    permission_required = 'library.change_'
    template_name = 'library/update.html'
    form_class = AttributeForm


class FrontpageView(TemplateView):
    template_name = 'frontpage.html'
