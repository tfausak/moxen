"""Django URL configuration.
"""
from django.conf.urls.defaults import patterns, url
from magic.views import CardDetailView, CardListView, SearchView


urlpatterns = patterns('magic.views',
    url('^$', 'index', name='index'),
    url('^cards/$', CardListView.as_view(), name='card_list'),
    url('^card/(?P<slug>[-\w]+)/$', CardDetailView.as_view(),
        name='card_detail'),
    url('^search/$', SearchView.as_view(), name='search'),
    url('^accounts/profile/$', 'profile', name='profile'),
)
