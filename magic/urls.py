# pylint: disable=C0103,E1120
from django.conf.urls.defaults import patterns, url
from magic.views import (CardDetailView, CardListView, SearchView,
    SetDetailView, SetListView)


urlpatterns = patterns('magic.views',
    url('^$', 'index', name='index'),
    url('^cards/$', CardListView.as_view(), name='card_list'),
    url('^cards/(?P<slug>[-\w]+)/$', CardDetailView.as_view(),
        name='card_detail'),
    url('^search/$', SearchView.as_view(), name='search'),
    url('^sets/$', SetListView.as_view(), name='set_list'),
    url('^sets/(?P<slug>[-\w]+)/$', SetDetailView.as_view(),
        name='set_detail'),
    url('^users/settings/$', 'profile', name='profile'),
)
