"""RPGuru Library views"""

from django.views.generic import CreateView, UpdateView, DetailView, TemplateView

from changerequest.views import PermissionMessageMixin, HistoryFormViewMixin

from .models import Platform
from .forms import PlatformCreateForm, PlatformUpdateForm


class PlatformModelFormMixin:
    model = Platform

    def get_success_url(self):
        return self.object.get_absolute_url('platform/update')


class PlatformCreateView(PermissionMessageMixin, HistoryFormViewMixin, PlatformModelFormMixin, CreateView):
    permission_required = 'library.add_platform'
    template_name = 'library/platform/create.html'
    form_class = PlatformCreateForm


class PlatformUpdateView(PermissionMessageMixin, HistoryFormViewMixin, PlatformModelFormMixin, UpdateView):
    permission_required = 'library.change_platform'
    template_name = 'library/platform/update.html'
    form_class = PlatformUpdateForm


class FrontpageView(TemplateView):
    template_name = 'frontpage.html'
