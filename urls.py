from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin


admin.autodiscover()
urlpatterns = patterns('',
    url('^admin/doc/', include('django.contrib.admindocs.urls')),
    url('^admin/', include(admin.site.urls)),
)
