from django.conf.urls.defaults import patterns, include
from django.contrib import admin


admin.autodiscover()
urlpatterns = patterns('',
    ('^admin/doc/', include('django.contrib.admindocs.urls')),
    ('^admin/', include(admin.site.urls)),
)
