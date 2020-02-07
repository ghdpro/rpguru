"""RPGuru Library URLs"""

from django.urls import path

from library.forms import PlatformForm
from library.models import Platform, Franchise, Company, Genre
from library.views import AttributeCreateView, AttributeUpdateView, AttributeListView, AttributeDetailView, \
    PlatformArtworkView


platform_urls = [
    path('create', AttributeCreateView.as_view(model=Platform, form_class=PlatformForm), name='create'),
    path('browse', AttributeListView.as_view(model=Platform), name='browse'),
    path('<slug:slug>/edit', AttributeUpdateView.as_view(model=Platform, form_class=PlatformForm), name='update'),
    path('<slug:slug>/artwork', PlatformArtworkView.as_view(), name='artwork'),
    path('<slug:slug>', AttributeDetailView.as_view(model=Platform), name='detail'),
]

franchise_urls = [
    path('create', AttributeCreateView.as_view(model=Franchise), name='create'),
    path('browse', AttributeListView.as_view(model=Franchise), name='browse'),
    path('<slug:slug>/edit', AttributeUpdateView.as_view(model=Franchise), name='update'),
    path('<slug:slug>', AttributeDetailView.as_view(model=Franchise), name='detail'),  # TODO: customize view
]

company_urls = [
    path('create', AttributeCreateView.as_view(model=Company), name='create'),
    path('browse', AttributeListView.as_view(model=Company), name='browse'),
    path('<slug:slug>/edit', AttributeUpdateView.as_view(model=Company), name='update'),
    path('<slug:slug>', AttributeDetailView.as_view(model=Company), name='detail'),  # TODO: customize view
]

genre_urls = [
    path('create', AttributeCreateView.as_view(model=Genre), name='create'),
    path('browse', AttributeListView.as_view(model=Genre), name='browse'),
    path('<slug:slug>/edit', AttributeUpdateView.as_view(model=Genre), name='update'),
    path('<slug:slug>', AttributeDetailView.as_view(model=Genre), name='detail'),
]
