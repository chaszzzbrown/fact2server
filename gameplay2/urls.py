from django.conf.urls import include, url

from . import views

urlpatterns = [

	url(r'^player/(?P<pk>[0-9]+)/begin_new_unsaved_game/$', views.player_begin_unsaved_game),
	url(r'^player/(?P<pk>[0-9]+)/begin_new_game/$', views.player_begin_game),
	url(r'^player/(?P<pk>[0-9]+)/end_current_game/$', views.player_end_game),
	
	url(r'^player/(?P<pk>[0-9]+)/$', views.player_info),
	url(r'^player/$', views.player_info),

	url(r'^game_play/(?P<pk>[0-9]+)/$', views.game_play),

	url(r'^game_settings/$', views.game_settings),

	url(r'^track_article/$', views.track_article),

	url(r'^get_article_stats/$', views.get_article_stats),

]