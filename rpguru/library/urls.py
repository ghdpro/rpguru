"""RPGuru Library URLs"""

from django.urls import path

from library.forms import PlatformForm
from library.models import Platform, PlatformArtwork, Franchise, FranchiseArtwork, \
    Company, CompanyArtwork, Genre, GenreArtwork
from library.views import AttributeCreateView, AttributeUpdateView, AttributeListView, AttributeDetailView, \
    AttributeArtworkView


def generate_urls(model, artwork, form=None) -> list:
    # :create
    if form is not None:
        result = [
            path('create', AttributeCreateView.as_view(model=model, form_class=form), name='create'),
        ]
    else:
        result = [
            path('create', AttributeCreateView.as_view(model=model), name='create'),
        ]
    # :browse
    result.append(path('browse', AttributeListView.as_view(model=model), name='browse'))
    # :update
    if form is not None:
        result.append(path('<slug:slug>/edit',
                           AttributeUpdateView.as_view(model=model, form_class=form), name='update'))
    else:
        result.append(path('<slug:slug>/edit',
                           AttributeUpdateView.as_view(model=model), name='update'))
    # :artwork
    result.append(
        path('<slug:slug>/artwork',
             AttributeArtworkView.as_view(model=model, artwork=artwork), name='artwork')
    )
    # :detail
    result.append(path('<slug:slug>', AttributeDetailView.as_view(model=model), name='detail'))
    return result


platform_urls = generate_urls(Platform, PlatformArtwork, PlatformForm)
franchise_urls = generate_urls(Franchise, FranchiseArtwork)
company_urls = generate_urls(Company, CompanyArtwork)
genre_urls = generate_urls(Genre, GenreArtwork)
