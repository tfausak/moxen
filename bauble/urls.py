from bauble.forms import UserProfileForm
from bauble.models import UserProfile
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from magic.models import Card
from registration.forms import RegistrationFormUniqueEmail


admin.autodiscover()
urlpatterns = patterns('',
    ('', include('magic.urls')),

    url('^users/settings/$', 'bauble.views.profile', name='profile'),
    ('^users/register/$', 'registration.views.register',
        {'form_class': RegistrationFormUniqueEmail}, 'registration_register'),
    ('^users/', include('registration.urls')),
    ('^users/create/', 'profiles.views.create_profile',
        {'form_class': UserProfileForm}, 'profiles_profile_create'),
    ('^users/edit/', 'profiles.views.edit_profile',
        {'form_class': UserProfileForm}, 'profiles_profile_edit'),
    ('^users/', include('profiles.urls')),

    ('^admin/', include(admin.site.urls)),
    ('^sitemap[.]xml', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {
            'cards': GenericSitemap({'queryset': Card.objects.all()}),
            'users': GenericSitemap({'queryset': UserProfile.objects.all()}),
        }}, 'sitemap'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        ('^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT, 'show_indexes': True})
    )
