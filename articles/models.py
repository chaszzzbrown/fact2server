from django.db import models

import re
import datetime

# Create your models here.

class Article(models.Model):

	NEWS = 'news'
	NOT_NEWS = 'notNews'
	ADVERTISING = 'advertising'
	OPINION = 'opinion'
	ENTERTAINMENT = 'entertainment'
	ARTICLE_TYPES = (
		(NEWS, 'News'),
		(NOT_NEWS, 'Not News'),
		(ADVERTISING, 'Advertising'),
		(OPINION, 'Opinion'),
		(ENTERTAINMENT, 'Entertainment'),
		)
	DIFFICULTIES = tuple((x,x) for x in ("easy", "medium", "hard"))
	LAYOUTS = tuple(('layout%d'%i, 'Layout %d'%i) for i in range(1,6))

	enabled = models.BooleanField(default=True)

	article_type = models.CharField(max_length=32, choices=ARTICLE_TYPES, default='news')
	difficulty = models.CharField(max_length=16, choices=DIFFICULTIES, default='easy')
	layout = models.CharField(max_length=16, choices=LAYOUTS, default='layout1')

	headline = models.TextField(default='', blank=True)
	photo = models.ImageField(blank=True)
	chunk1 = models.TextField(default='', blank=True)
	chunk2 = models.TextField(default='', blank=True)
	chunk3 = models.TextField(default='', blank=True)

	# for the "show info" dialog
	source = models.TextField(max_length=160, blank=True, default='')
	author = models.TextField(max_length=160, blank=True, default='')
	references = models.TextField(blank=True, default='')
	tone = models.CharField(max_length=80, default='', blank=True)

	# adminn-ing
	source_URL = models.TextField(default='', blank=True)
	created_date = models.DateField(auto_now_add=True)
	modified_date = models.DateField(auto_now=True)

	# factv2 reorganized fields
	body = models.TextField(default='', blank=True)
	articleType = models.CharField(max_length=32, choices=((NEWS, 'News'), (NOT_NEWS, 'Not News')), default='news')
	sourceHint = models.TextField(default='', blank=True)
	payoffSourceLabel = models.TextField(max_length=160, blank=True, default='')
	payoffSourceUrl = models.TextField(blank=True, default='')
	payoffContent = models.TextField(default='', blank=True)

	class Meta:
		ordering = ('-created_date',)

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
				'tone': self.tone,
			},
			'source_URL': self.source_URL,
			'pk': self.pk,
		}

	def forJSONList(self):
		return { 
			'article_id': self.id_from_pk(),
			'article_type': self.article_type,
			'difficulty': self.difficulty,
			'headline': self.headline,
			'pk': self.pk,
		}

	def __unicode__(self):
		return '('+self.id_from_pk()+') '+self.headline+' ['+self.article_type+']'

	def forJSON_V2(self):
		return {
			'article_id': self.id_from_pk(),
			'articleType': self.articleType,
			'headline': self.headline,
			'photo_url': self.photo.url if self.photo else '/media/default_im.png',
			'body': self.body,
			'sourceHint': self.sourceHint,
			'payoffSourceLabel': self.payoffSourceLabel,
			'payoffSourceUrl': self.payoffSourceUrl,
			'payoffContent': self.payoffContent,
			'pk': self.pk,
		}

	def updateToV2(self):

		def cleanupEOL(s):
			return s.replace('\r\n', '\n').strip()

		self.articleType = Article.NEWS if self.article_type==Article.NEWS else Article.NOT_NEWS

		chunks = [cleanupEOL(chunk) for chunk in [self.chunk1, self.chunk2, self.chunk3]]
		self.body = '\n\n'.join(chunk for chunk in chunks if chunk)

		self.sourceHint = '\n\n'.join(sline for sline in cleanupEOL(self.source).split('\n') if sline)

		if self.references:
			refLines = [rLine for rLine in cleanupEOL(self.references).split('\n') if rLine]
			sourceName = refLines[0]

			if sourceName.startswith('Source:'):
				self.payoffSourceLabel = sourceName.replace('Source:','').strip()
				refLines = refLines[1:]

			self.payoffContent = '\n\n'.join(refLines)

		self.payoffSourceUrl = self.source_URL.split('\n')[0].replace('"','').strip()





