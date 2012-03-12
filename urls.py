"""Django URL configuration.
"""
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from django.contrib import admin
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
    ('^profiles/', include('profiles.urls')),
    ('', include('magic.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        ('^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': './static/', 'show_indexes': True})
    )
