"""Django URL configuration.
"""
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from magic.forms import UserProfileForm
from magic.models import Card, UserProfile
from registration.forms import RegistrationFormUniqueEmail


admin.autodiscover()
urlpatterns = patterns('',
    ('', include('magic.urls')),

    # Django's built-in admin
    ('^admin/doc/', include('django.contrib.admindocs.urls')),
    ('^admin/', include(admin.site.urls)),

    # django-registration
    ('^users/register/$', 'registration.views.register',
        {'form_class': RegistrationFormUniqueEmail}, 'registration_register'),
    ('^users/', include('registration.urls')),

    # django-profiles
    ('^users/create/', 'profiles.views.create_profile',
        {'form_class': UserProfileForm}, 'profiles_profile_create'),
    ('^users/edit/', 'profiles.views.edit_profile',
        {'form_class': UserProfileForm}, 'profiles_profile_edit'),
    ('^users/', include('profiles.urls')),

    # Django's built-in sitemap
    ('^sitemap[.]xml', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {
            'cards': GenericSitemap({'queryset': Card.objects.all()}),
            'users': GenericSitemap({'queryset': UserProfile.objects.all()}),
        }}, 'sitemap'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        ('^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': './static/', 'show_indexes': True})
    )
