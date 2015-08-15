from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^player/(?P<pk>A[0-9]+)/$', views.player_info),
	url(r'^player/$', views.player_info),

]