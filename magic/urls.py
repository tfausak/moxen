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
    url('^accounts/register/$', 'register', name='register'),
)


urlpatterns += patterns('django.contrib.auth.views',
    url('^accounts/login/$', 'login', name='login'),
    url('^accounts/logout/$', 'logout', name='logout'),
    url('^accounts/password/change/$', 'password_change',
        name='password_change'),
    url('^accounts/password/change/success/$', 'password_change_done',
        name='password_change_done'),
    url('^accounts/password/reset/$', 'password_reset',
        name='password_reset'),
    url('^accounts/password/reset/sent/$', 'password_reset_done',
        name='password_reset_done'),
    url('^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'password_reset_confirm', name='password_reset_confirm'),
    url('^accounts/password/reset/success/$', 'password_reset_complete',
        name='password_reset_complete'),
)
