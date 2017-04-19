from django.db import models
from django.utils import timezone

import datetime
import json

from articles.models import Article

class PlayerInfo(models.Model):

	GENDERS = (
		('M', 'male'),
		('F', 'female'),
		('T', 'trans'),
		('O', 'other'),
	)
	
	EDUCATION = tuple((item, item) for item in "HS diploma, some college, BS/BA, MS/MA, PhD, other".split(', '))

	SAVVY_LIKERT = (
		(1, '1 - not savvy'),
		(2, '2'),
		(3, '3'),
		(4, '4'),
		(5, '5 - very savvy'),
	)

	username = models.CharField(max_length=64, unique=True)
	
	age = models.IntegerField(default=10)
	gender = models.CharField(choices=GENDERS, default='M', max_length=8)
	education = models.CharField(choices=EDUCATION, default='other', max_length=32)
	computer_use = models.IntegerField(default=0)
	news_media_savvy = models.IntegerField(default=3, choices=SAVVY_LIKERT)
	news_source = models.CharField(max_length=36, default='', blank=True)

	# adminn-ing
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	has_completed_survey = models.BooleanField(default=False)

	is_anonymous = models.BooleanField(default=False)

	current_game = models.ForeignKey('GamePlay', null=True, blank=True)

	def __unicode__(self):
		return 'username '+self.username

class GameSettings(models.Model):

	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	game_settings_json = models.TextField(default='{}', blank=True)

class GamePlay(models.Model):

	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	player_info = models.ForeignKey('PlayerInfo', related_name='game_plays')

	is_completed = models.BooleanField(default=False)
	was_cancelled = models.BooleanField(default=False)

	game_settings_json = models.TextField(default='{}', blank=True)

	game_state_json = models.TextField(default='{}', blank=True)

	# these fields will be manually updated by the client side
	total_score = models.IntegerField(default=0)
	total_time_seconds = models.IntegerField(default=0)
	total_articles_played = models.IntegerField(default=0)
	total_articles_correct = models.IntegerField(default=0)

	maximum_score = models.IntegerField(default=0)
	maximum_articles_played = models.IntegerField(default=0)

	@property
	def game_state(self):
		return json.loads(self.game_state_json)

	@game_state.setter
	def game_state(self, value):
		self.game_state_json = json.dumps(value)

	@property
	def game_settings(self):
		return json.loads(self.game_settings_json)

	@game_settings.setter
	def game_settings(self, value):
		self.game_settings_json = json.dumps(value)

	def __unicode__(self):
		return str(self.created_date)+'  '+self.game_outcome

	@property
	def game_outcome(self):
		if self.is_completed:
			return 'completed'
		elif self.was_cancelled:
			return 'cancelled'
		elif (timezone.now()-self.created_date).total_seconds()>48*3600:
			return 'abandoned'
		else:
			return 'inPlay'

class ArticlePlay(models.Model):
	created_date = models.DateTimeField(auto_now_add=True)

	total_time_seconds = models.IntegerField(default=0)
	was_correct = models.BooleanField(default=False)
	showed_hint = models.BooleanField(default=False)

	article = models.ForeignKey(Article)
	player_info = models.ForeignKey(PlayerInfo)

