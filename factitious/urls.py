"""factitious URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from articles import urls as article_urls
from gameplay import urls as gameplay_urls
from f2auth import urls as f2auth_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/article/', include(article_urls)),
    url(r'^api/gameplay/', include(gameplay_urls)),
    url(r'^api/f2auth/', include(f2auth_urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
