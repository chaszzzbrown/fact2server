from articles.models import *
from PIL import Image
from django.conf import settings
import os
import glob

def getUsedImages():
	return [a.photo.url.replace(settings.MEDIA_URL, '') for a in Article.objects.all()]

def getUnusedImages():

	allImages = []
	for sfx in ['*.jpg', '*.JPG', '*.JPEG', '*.jpeg', '*.png', '*.PNG', '*.gif', '*.GIF']:
		allImages.extend(glob.glob(os.path.join(settings.MEDIA_ROOT, sfx)))

	usedImages = [os.path.join(settings.MEDIA_ROOT, im) for im in getUsedImages()]

	return [im for im in allImages if im not in usedImages]

def removeUnusedImages():
	for im in getUnusedImages():
		os.remove(im)

def resizeImages():

	for imName in getUsedImages():
		im = Image.open(os.path.join(settings.MEDIA_ROOT, imName))

		width, height = im.size

		maxDimension = MAX_IMAGE_SIZE
		scaling = min(maxDimension/width, maxDimension/height)
		scaling = maxDimension/width

		if scaling<1.0:
			print 'resizing '+imName
			im.thumbnail((scaling*width, scaling*height), Image.ANTIALIAS)
			im.save(os.path.join(settings.MEDIA_ROOT, imName))

def cleanUpMedia():
	removeUnusedImages()
	resizeImages()
