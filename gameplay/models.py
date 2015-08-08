from django.db import models

from articles.models import Article

# Create your models here.

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

	username = models.CharField(max_length=32, unique=True)
	
	age = models.IntegerField(default=10)
	gender = models.CharField(choices=GENDERS, default='M')
	education = models.CharField(choices=EDUCATION, default='other')
	computer_use = models.IntegerField(default=0)
	news_media_savvy = models.IntegerField(default=3, choices=SAVVY_LIKERT)
	news_source = models.CharField(max_length=36)

	# adminn-ing
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	# maybe...?
	current_game = models.ForeignKey('GameInfo', null=True)

	def start_new_game(self, difficulty, max_stories, feedback_version, scoring_version):
		pass

	def get_random_unplayed_article(self, difficulty=None, exclude_articles=None):
		pass

	def end_game(self):
		pass

class GameInfo(models.Model):

	player_info = models.ForeignKey('PlayerInfo')

	difficulty = models.CharField(max_length=16, choices=Article.DIFFICULTIES)
	max_stories = models.IntegerField(default=10)

	feedback_version = models.CharField(max_length=16, choices=(('friendly', 'friendly'), ('snarky', 'snarky'),), default='friendly')
	scoring_version = models.IntegerField(default=1)

	created_time = models.DateTimeField(auto_now_add=True)
	modified_time = models.DateTimeField(auto_now=True)

	current_round = models.ForeignKey('GameRound', null=True)

	is_completed = models.BooleanField(default=Fals e)

	def started_articles(self):
		pass

	def start_new_round(self):
		pass

	def end_round(self, user_guess):
		pass

class GameRound(models.Model):

	player_info = models.ForeignKey('PlayerInfo')
	game_info = models.ForeignKey('GameInfo')

	article = models.ForeignKey('Article')

	start_time = models.DateTimeField(auto_now_add=True)
	end_time = models.DateTimeField(auto_now=True)

	is_completed = models.BooleanField(default=False)

	chunk2_requested = models.BooleanField(default=False)
	chunk3_requested = models.BooleanField(default=False)
	show_info_requested = models.BooleanField(default=False)

	player_guess = models.CharField(max_length=16, default='')

