from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from tictac.views import board, play, clear_board, home, get_player_letter, get_player_name

urlpatterns = patterns('',
    url(r'^$',home , name="home"),
    url(r'^board/$', board, name="board"),
    url(r'^play/$', play, name="play"),
    url(r'^get_player_letter/$', get_player_letter, name='player_letter'),
    url(r'^get_player_name/$', get_player_name, name='player_name')
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)