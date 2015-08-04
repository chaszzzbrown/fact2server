from django.db import models

import re
import datetime

# Create your models here.

class Article(models.Model):

	NEWS = 'news'
	ADVERTISING = 'advertising'
	OPINION = 'opinion'
	ENTERTAINMENT = 'entertainment'
	ARTICLE_TYPES = (
		(NEWS, 'News'),
		(ADVERTISING, 'Advertising'),
		(OPINION, 'Opinion'),
		(ENTERTAINMENT, 'Entertainment'),
		)
	DIFFICULTIES = tuple((x,x) for x in ("easy", "medium", "hard"))
	LAYOUTS = tuple(('layout%d'%i, 'Layout %d'%i) for i in range(1,6))

	enabled = models.BooleanField(default=True)

	article_type = models.CharField(max_length=32, choices=ARTICLE_TYPES)
	difficulty = models.CharField(max_length=16, choices=DIFFICULTIES)
	layout = models.CharField(max_length=16, choices=LAYOUTS)

	headline = models.TextField(default='', blank=True)
	photo = models.ImageField(blank=True)
	chunk1 = models.TextField(default='', blank=True)
	chunk2 = models.TextField(default='', blank=True)
	chunk3 = models.TextField(default='', blank=True)

	# for the "show info" dialog
	source = models.TextField(max_length=160, blank=True, default='')
	author = models.TextField(max_length=160, blank=True, default='')
	references = models.TextField(blank=True, default='')

	# adminn-ing
	created_date = models.DateField(auto_now_add=True)
	modified_date = models.DateField(auto_now=True)

	@staticmethod
	def pk_from_id(article_id):
		try:
			return int(re.search(r'A[0]+([0-9]+)$', article_id).groups()[0])
		except AttributeError:
			return None

	def id_from_pk(self):
		return 'A'+str(self.pk).rjust(5,'0')


	def forJSON(self):
		return {
			'article_id': self.id_from_pk(),
			'article_type': self.article_type,
			'difficulty': self.difficulty,
			'layout': self.layout,
			'headline': self.headline,
			'photo_url': self.photo.url if self.photo else '/media/default_im.png',
			'chunk1': self.chunk1,
			'chunk2': self.chunk2,
			'chunk3': self.chunk3,
			'info': {
				'source': self.source,
				'author': self.author,
				'references': self.references,
			},
		}

	def forJSONList(self):
		return { 
			'article_id': self.id_from_pk(),
			'article_type': self.article_type,
			'difficulty': self.difficulty,
			'headline': self.headline,
		}

	def __unicode__(self):
		return '('+self.id_from_pk()+') '+self.headline




