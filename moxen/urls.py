# pylint: disable=C0103,E1120
from app.moxen.forms import UserRegistrationForm, UserProfileForm
from app.moxen.models import UserProfile
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template',
        {'template': 'base.html'}, 'index'),
    url(r'', include('app.magic.urls')),

    # Registration
    url(r'^users/register/$', 'registration.views.register',
        {
            'backend': 'registration.backends.default.DefaultBackend',
            'form_class': UserRegistrationForm,
        }, 'registration_register'),
    url(r'^users/', include('registration.backends.default.urls')),

    # Profiles
    url(r'^users/delete/$', 'app.moxen.views.delete_user',
        name='delete_user'),
    url(r'^users/create/', 'profiles.views.create_profile',
        {'form_class': UserProfileForm}, 'profiles_profile_create'),
    url(r'^users/edit/', 'profiles.views.edit_profile',
        {'form_class': UserProfileForm}, 'profiles_profile_edit'),
    url(r'^users/', include('profiles.urls')),

    # Sitemap
    url(r'^sitemap[.]xml', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {
            'users': GenericSitemap({'queryset': UserProfile.objects.all()}),
        }}, 'sitemap'),

    # Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
