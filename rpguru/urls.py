"""RPGuru URL Configuration"""

from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from allauth.account import views as account

from library.urls import platform_urls, franchise_urls, company_urls, genre_urls, game_urls
from library.views import SearchView, FrontpageView
from library.sitemap import sitemaps


# URLs for django-allauth/account have been redefined here to remove the ending slash
account_patterns = [
    path('signup', account.signup, name='account_signup'),
    path('login', account.login, name='account_login'),
    path('logout', account.logout, name='account_logout'),
    path('password/change', account.password_change, name='account_change_password'),
    path('password/set', account.password_set, name='account_set_password'),
    path('inactive', account.account_inactive, name='account_inactive'),
    # E-mail
    path('email', account.email, name='account_email'),
    path('confirm-email', account.email_verification_sent, name='account_email_verification_sent'),
    re_path(r'confirm-email/(?P<key>[-:\w]+)', account.confirm_email, name='account_confirm_email'),
    # Password reset
    path('password/reset', account.password_reset, name='account_reset_password'),
    path('password/reset/done', account.password_reset_done, name='account_reset_password_done'),
    re_path(r'password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)', account.password_reset_from_key,
            name='account_reset_password_from_key'),
    path('password/reset/key/done', account.password_reset_from_key_done, name='account_reset_password_from_key_done'),
    # No profile page at the moment
    path('profile', RedirectView.as_view(url='/'), name='account_profile'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(account_patterns)),
    path('history/', include('changerequest.urls')),
    path('platform/', include((platform_urls, 'platform'))),
    path('series/', include((franchise_urls, 'franchise'))),
    path('company/', include((company_urls, 'company'))),
    path('genre/', include((genre_urls, 'genre'))),
    path('game/', include((game_urls, 'game'))),
    path('search', SearchView.as_view(), name='search'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', FrontpageView.as_view(), name='frontpage')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))] + \
                   static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
