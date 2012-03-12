"""Django URL configuration.
"""
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from django.contrib import admin


admin.autodiscover()
urlpatterns = patterns('',
    ('^admin/doc/', include('django.contrib.admindocs.urls')),
    ('^admin/', include(admin.site.urls)),
    ('^accounts/', include('registration.backends.default.urls')),
    ('', include('magic.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        ('^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': './static/', 'show_indexes': True})
    )
