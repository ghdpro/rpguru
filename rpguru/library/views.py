"""RPGuru Library views"""

from django import forms
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView

from changerequest.views import PermissionMessageMixin, HistoryFormViewMixin, HistoryFormsetViewMixin, \
    ListQueryStringMixin
from artwork.views import ArtworkActiveMixin

from .forms import AttributeForm, GameForm, GameArtworkForm, GameArtworkFormset
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
        # The 'first' game context data is used for Social Meta cards in case main object doesn't have an image
        if self.model._meta.model_name == 'franchise':
            context['main'] = Game.objects.custom().filter(franchise_main=context['object'])
            context['side'] = Game.objects.custom().filter(franchise_side=context['object'])
            if len(context['main']) > 0:
                context['first'] = context['main'][0]
            elif len(context['side']) > 0:
                context['first'] = context['side'][0]
        elif self.model._meta.model_name == 'company':
            context['developed'] = Game.objects.custom().filter(developer=context['object'])
            context['published'] = Game.objects.custom().filter(publisher=context['object'])\
                .exclude(developer=context['object'])
            if len(context['developed']) > 0:
                context['first'] = context['developed'][0]
            elif len(context['published']) > 0:
                context['first'] = context['published'][0]
        else:
            context['games'] = Game.objects.custom().filter(**{self.model._meta.model_name: context['object']})
            if len(context['games']) > 0:
                context['first'] = context['games'][0]
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


class GameCreateView(PermissionMessageMixin, HistoryFormViewMixin, CreateView):
    permission_required = 'library.add_game'
    template_name = 'library/game/create.html'
    form_class = GameForm
    model = Game

    def get_success_url(self):
        return reverse('game:update', kwargs={'pk': self.object.pk})


class GameUpdateView(PermissionMessageMixin, HistoryFormViewMixin, UpdateView):
    permission_required = 'library.change_game'
    template_name = 'library/game/update.html'
    form_class = GameForm
    model = Game

    def get_success_url(self):
        return reverse('game:update', kwargs={'pk': self.object.pk})


class GameArtworkView(PermissionMessageMixin, ArtworkActiveMixin, HistoryFormsetViewMixin, UpdateView):
    permission_required = 'library.add_gameartwork'
    template_name = 'library/game/artwork.html'
    form_class = GameArtworkForm
    formset_class = GameArtworkFormset
    model = Game

    def get_success_url(self):
        return reverse('game:artwork', kwargs={'pk': self.object.pk})


class SearchView(ListQueryStringMixin, ListView):
    template_name = 'library/search.html'
    paginate_by = 10
    model = Game
    queryset = Game.objects.custom()

    def get(self, request, *args, **kwargs):
        # If searching for empty string, redirect to Frontpage instead
        search = self.request.GET.get('q', '').strip()
        if len(search) == 0:
            return redirect('frontpage')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('q', '').strip()
        qs = qs.filter(Q(title__icontains=search) |
                       Q(developer__name__icontains=search) |
                       Q(publisher__name__icontains=search))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q', '').strip()
        return context


class FrontpageView(TemplateView):
    template_name = 'frontpage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games'] = Game.objects.custom().all()[0:5]
        if len(context['games']) > 0:
            context['first'] = context['games'][0]
        return context
