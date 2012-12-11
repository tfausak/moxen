# pylint: disable=C0103
from django.conf.urls.defaults import patterns, url
from app.magic.views import (CardDetailView, CardListView,
    CollectionDetailView, DeckDetailView, DeckListView, PrintingDetailView,
    SearchView, SetDetailView, SetListView)

urlpatterns = patterns('app.magic.views',
    url(r'^cards/$', CardListView.as_view(), name='card_list'),
    url(r'^cards/(?P<slug>[-\w]+)/$', CardDetailView.as_view(),
        name='card_detail'),
    url(r'^decks/$', DeckListView.as_view(), name='deck_list'),
    url(r'^decks/(?P<pk>\d+)/$', DeckDetailView.as_view(), name='deck_detail'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^sets/$', SetListView.as_view(), name='set_list'),
    url(r'^sets/(?P<set_slug>[-\w]+)/(?P<number>\d+)-(?P<card_slug>[-\w]+)/$',
        PrintingDetailView.as_view(), name='printing_detail'),
    url(r'^sets/(?P<slug>[-\w]+)/$', SetDetailView.as_view(),
        name='set_detail'),
    url(r'^users/(?P<username>\w+)/collection/$',
        CollectionDetailView.as_view(), name='collection_detail'),
)
