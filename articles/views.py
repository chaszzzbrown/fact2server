from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed

from . models import Article

import json

# Create your views here.

def article_json(request, article_id):
	pk = Article.pk_from_id(article_id)

	article = Article.objects.get(pk=pk)
	return HttpResponse(json.dumps(article.forJSON()))

def all_articles(request):

	res = [a.id_from_pk() for a in Article.objects.all()]

	return HttpResponse(json.dumps(res))
	