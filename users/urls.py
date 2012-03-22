# pylint: disable=C0103,E1120
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('users.views',
    url('^users/settings/$', 'profile', name='profile'),
)
