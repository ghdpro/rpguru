"""RPGuru Library URLs"""

from django.urls import path

from library.views import (PlatformCreateView, PlatformUpdateView, FrontpageView)


platform_urls = [
    path('create', PlatformCreateView.as_view(), name='create'),
    path('<slug:slug>/edit', PlatformUpdateView.as_view(), name='update'),
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
