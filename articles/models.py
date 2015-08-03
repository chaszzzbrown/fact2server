from django.db import models

import re

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

	article_type = models.CharField(max_length=32, choices=ARTICLE_TYPES)
	difficulty = models.CharField(max_length=16, choices=DIFFICULTIES)
	layout = models.CharField(max_length=16, choices=LAYOUTS)

	headline = models.TextField(default='', blank=True)
	photo = models.ImageField(blank=True)
	chunk1 = models.TextField(default='', blank=True)
	chunk2 = models.TextField(default='', blank=True)
	chunk3 = models.TextField(default='', blank=True)

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
			'photo_url': self.photo.url if self.photo else '',
			'chunk1': self.chunk1,
			'chunk2': self.chunk2,
			'chunk3': self.chunk3,
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




