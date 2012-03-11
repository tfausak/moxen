from django.conf.urls.defaults import patterns, url
from magic.views import CardListView


urlpatterns = patterns('magic.views',
    url('^$', 'index', name='index'),
    url('^cards/$', CardListView.as_view(), name='card_list'),
)
