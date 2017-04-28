from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed
from django.core.files.storage import FileSystemStorage

import json
from PIL import Image

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . models import Article, MAX_IMAGE_SIZE

import json

# Create your views here.

def article_json(request, article_id):
	pk = article_id # Article.pk_from_id(article_id)

	article = Article.objects.get(pk=pk)
	if not article.body:
		article.updateToV2()
	return HttpResponse(json.dumps(article.forJSON_V2()))

def all_articles(request):

	res = [a.forJSONList() for a in Article.objects.all().order_by('-pk')]

	return HttpResponse(json.dumps(res))


@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def get_blank_article(request):
	blank = Article()
	return HttpResponse(json.dumps(blank.forJSON_V2()))

@api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
def put_article(request):

	if 'pk' in request.POST:
		article = Article.objects.get(pk=request.POST['pk'])
	else:
		article = Article.objects.create()

	photoFile = request.FILES.get('photo', None)

	if photoFile:

		im = Image.open(photoFile)

		width, height = im.size

		maxDimension = MAX_IMAGE_SIZE
		scaling = min(maxDimension/width, maxDimension/height)
		scaling = maxDimension/width

		if scaling<1.0:
			im.thumbnail((scaling*width, scaling*height), Image.ANTIALIAS)

		fs = FileSystemStorage()

		with fs.open(photoFile.name, 'wb') as pf:
			im.save(pf)

		article.photo = fs.url(photoFile.name)

	for key in request.POST.keys():
		if key != 'pk':
			setattr(article, key, request.POST[key])

	article.save()

	return HttpResponse(json.dumps(article.forJSON_V2()))

