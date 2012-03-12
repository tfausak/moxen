"""Django URL configuration.
"""
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from magic.forms import UserProfileForm
from magic.models import Card
from registration.forms import RegistrationFormUniqueEmail


admin.autodiscover()
urlpatterns = patterns('',
    ('^admin/doc/', include('django.contrib.admindocs.urls')),
    ('^admin/', include(admin.site.urls)),
    ('^accounts/register/$', 'registration.views.register', {
            'backend': 'registration.backends.default.DefaultBackend',
            'form_class': RegistrationFormUniqueEmail,
        }, 'registration_register'),
    ('^accounts/', include('registration.backends.default.urls')),
    ('^profiles/create/', 'profiles.views.create_profile',
        {'form_class': UserProfileForm}, 'profiles_profile_create'),
    ('^profiles/edit/', 'profiles.views.edit_profile',
        {'form_class': UserProfileForm}, 'profiles_profile_edit'),
    ('^profiles/', include('profiles.urls')),
    ('^sitemap[.]xml', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {
            'cards': GenericSitemap({'queryset': Card.objects.all()}),
        }}, 'sitemap'),
    ('', include('magic.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        ('^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': './static/', 'show_indexes': True})
    )
