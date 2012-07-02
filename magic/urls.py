from django.conf.urls.defaults import patterns, url
from magic.views import (CardDetailView, CardListView, DeckDetailView,
    DeckListView, PrintingDetailView, SearchView, SetDetailView, SetListView)


urlpatterns = patterns('magic.views',
    url('^$', 'index', name='index'),
    url('^cards/$', CardListView.as_view(), name='card_list'),
    url('^cards/(?P<slug>[-\w]+)/$', CardDetailView.as_view(),
        name='card_detail'),
    url('^search/$', SearchView.as_view(), name='search'),
    url('^sets/$', SetListView.as_view(), name='set_list'),
    url('^sets/(?P<slug>[-\w]+)/$', SetDetailView.as_view(),
        name='set_detail'),
    url('^sets/(?P<set_slug>[-\w]+)/(?P<number>\d+)-(?P<card_slug>[-\w]+)/$',
        PrintingDetailView.as_view(), name='printing_detail'),
    url('^decks/$', DeckListView.as_view(), name='deck_list'),
    url('^decks/(?P<pk>\d+)/$', DeckDetailView.as_view(),
        name='deck_detail'),
)
