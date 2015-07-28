from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^id/(?P<article_id>A[0-9]+)/$', views.article_json),
	url(r'^list/$', views.all_articles),


]