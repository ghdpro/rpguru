"""RPGuru Library URLs"""

from django.urls import path

from library.models import Platform, Franchise, Company, Genre
from library.views import (AttributeCreateView, AttributeUpdateView, AttributeDetailView)


platform_urls = [
    path('create', AttributeCreateView.as_view(model=Platform), name='create'),
    path('<slug:slug>/edit', AttributeUpdateView.as_view(model=Platform), name='update'),
    path('<slug:slug>', AttributeDetailView.as_view(model=Platform), name='detail'),
]

franchise_urls = [
    path('<slug:slug>', AttributeDetailView.as_view(model=Franchise), name='detail'),  # TODO: customize view
]

company_urls = [
    path('<slug:slug>', AttributeDetailView.as_view(model=Company), name='detail'),  # TODO: customize view
]

genre_urls = [
    path('<slug:slug>', AttributeDetailView.as_view(model=Genre), name='detail'),
]
