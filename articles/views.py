from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed
from django.core.files.storage import FileSystemStorage

import json
from PIL import Image

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . models import Article

import json

# Create your views here.

def article_json(request, article_id):
	pk = article_id # Article.pk_from_id(article_id)

	article = Article.objects.get(pk=pk)
	article.updateToV2()
	return HttpResponse(json.dumps(article.forJSON_V2()))

def all_articles(request):

	res = [a.forJSONList() for a in Article.objects.all()]

	return HttpResponse(json.dumps(res))


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def put_article(request):
	return HttpResponse('OK '+request.body)

@api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
def put_article_image(request):
	print "Trying"
	print request.POST.keys()

	pk = request.POST['pk']

	photoFile = request.FILES.get('photo', None)

	im = Image.open(photoFile)

	width, height = im.size

	maxDimension = 420.0
	scaling = min(maxDimension/width, maxDimension/height)
	scaling = maxDimension/width

	if scaling<1.0:
		im.thumbnail((scaling*width, scaling*height), Image.ANTIALIAS)
		print 'rescaled'

	fs = FileSystemStorage()

	print 'opening "'+photoFile.name+'"'
	with fs.open(photoFile.name, 'wb') as pf:
		print 'saving'
		im.save(pf)
		print 'saved'

	article = Article.objects.get(pk=pk)

	article.photo = fs.url(photoFile.name)
	article.save()


	return HttpResponse('OK '+fs.url(photoFile.name))