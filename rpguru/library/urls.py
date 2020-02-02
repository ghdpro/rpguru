"""RPGuru Library URLs"""

from django.urls import path

from library.models import Platform
from library.views import (AttributeCreateView, AttributeUpdateView, FrontpageView)


platform_urls = [
    path('create', AttributeCreateView.as_view(model=Platform), name='create'),
    path('<slug:slug>/edit', AttributeUpdateView.as_view(model=Platform), name='update'),
    path('<slug:slug>', FrontpageView.as_view(), name='detail'),  # TODO: replace with proper view
]

franchise_urls = [
    path('<slug:slug>', FrontpageView.as_view(), name='detail'),  # TODO: replace with proper view
]

company_urls = [
    path('<slug:slug>', FrontpageView.as_view(), name='detail'),  # TODO: replace with proper view
]

genre_urls = [
    path('<slug:slug>', FrontpageView.as_view(), name='detail'),  # TODO: replace with proper view
]
