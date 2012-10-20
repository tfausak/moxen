from bauble.forms import UserRegistrationForm, UserProfileForm
from bauble.models import UserProfile
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from magic.models import Card, Deck, Printing, Set
from magic.views import CollectionDetailView


admin.autodiscover()
urlpatterns = patterns('',
    ('', include('magic.urls')),

    url('^users/settings/$', 'bauble.views.profile', name='profile'),
    url('^users/delete/$', 'bauble.views.delete_account',
        name='delete_account'),
    ('^users/register/$', 'registration.views.register', {
            'backend': 'registration.backends.default.DefaultBackend',
            'form_class': UserRegistrationForm,
        }, 'registration_register'),
    ('^users/', include('registration.backends.default.urls')),
    ('^users/create/', 'profiles.views.create_profile',
        {'form_class': UserProfileForm}, 'profiles_profile_create'),
    ('^users/edit/', 'profiles.views.edit_profile',
        {'form_class': UserProfileForm}, 'profiles_profile_edit'),
    ('^users/', include('profiles.urls')),
    url(r'^users/(?P<username>\w+)/collection/$',
        CollectionDetailView.as_view(), name='collection_detail'),

    ('^admin/', include(admin.site.urls)),
    ('^sitemap[.]xml', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {
            'cards': GenericSitemap({'queryset': Card.objects.all()}),
            'decks': GenericSitemap({'queryset': Deck.objects.all()}),
            'printings': GenericSitemap({'queryset': Printing.objects.all()}),
            'sets': GenericSitemap({'queryset': Set.objects.all()}),
            'users': GenericSitemap({'queryset': UserProfile.objects.all()}),
        }}, 'sitemap'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        ('^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT, 'show_indexes': True})
    )
