"""RPGuru Library views"""

from django.views.generic import CreateView, UpdateView, DetailView, TemplateView

from changerequest.views import PermissionMessageMixin, HistoryFormViewMixin

from .models import Platform
from .forms import PlatformCreateForm, PlatformUpdateForm


class PlatformCreateView(PermissionMessageMixin, HistoryFormViewMixin, CreateView):
    permission_required = 'library.add_platform'
    template_name = 'library/platform/create.html'
    form_class = PlatformCreateForm
    model = Platform

    def get_success_url(self):
        return self.object.get_absolute_url('platform/update')


class PlatformUpdateView(PermissionMessageMixin, HistoryFormViewMixin, UpdateView):
    permission_required = 'library.change_platform'
    template_name = 'library/platform/update.html'
    form_class = PlatformUpdateForm
    model = Platform

    def get_success_url(self):
        return self.object.get_absolute_url('platform/update')


class FrontpageView(TemplateView):
    template_name = 'frontpage.html'
