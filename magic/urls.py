from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('magic.views',
    url('^$', 'index', name='index'),
)
