from django.conf.urls import include, url

from . import views
from rest_framework.authtoken import views as auth_views

urlpatterns = [
	url(r'^api-token-auth/', auth_views.obtain_auth_token),
]