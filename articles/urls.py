from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^id/A(?P<article_id>[0-9]+)/$', views.article_json),
	url(r'^(?P<article_id>[0-9]+)/$', views.article_json),
	url(r'^list/$', views.all_articles),
	url(r'^postarticle/$', views.put_article),
	url(r'^newarticle/$', views.get_blank_article),
]