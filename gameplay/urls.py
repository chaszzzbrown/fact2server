from django.conf.urls import include, url

from . import views

urlpatterns = [

	url(r'^player/(?P<pk>[0-9]+)/begin_new_game/$', views.player_begin_game),
	url(r'^player/(?P<pk>[0-9]+)/end_current_game/$', views.player_end_game),
	
	url(r'^player/(?P<pk>[0-9]+)/$', views.player_info),
	url(r'^player/$', views.player_info),

	url(r'^game_info/(?P<pk>[0-9]+)/start_new_round/$', views.game_start_round), # guess=<user's_guess>
	url(r'^game_info/(?P<pk>[0-9]+)/end_current_round/$', views.game_end_round), # guess=<user's_guess>
	url(r'^game_info/(?P<pk>[0-9]+)/$', views.game_info),

	url(r'^game_round/(?P<pk>[0-9]+)/$', views.game_round_info),
	url(r'^game_round_details/(?P<pk>[0-9]+)/$', views.game_round_full_info),

	url(r'^game_settings/(?P<settings_name>\w+)/$', views.game_settings),
	url(r'^article_stats/(?P<game_category>\w+)/$', views.article_stats),

	url(r'^game_stats/(?P<game_category>\w+)/$', views.game_stats),
	

]