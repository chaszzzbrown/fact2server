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

	username = models.CharField(max_length=64, unique=True)
	
	age = models.IntegerField(default=10)
	gender = models.CharField(choices=GENDERS, default='M', max_length=8)
	education = models.CharField(choices=EDUCATION, default='other', max_length=32)
	computer_use = models.IntegerField(default=0)
	news_media_savvy = models.IntegerField(default=3, choices=SAVVY_LIKERT)
	news_source = models.CharField(max_length=36)

	# adminn-ing
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	# maybe...?
	current_game = models.ForeignKey('GameInfo', null=True, blank=True)

	def start_new_game(self, difficulty, max_stories, feedback_version, scoring_version):
		pass

	def get_random_unplayed_article(self, difficulty=None, exclude_articles=None):
		pass

	def end_game(self):
		pass

	def __unicode__(self):
		return self.username

class GameInfo(models.Model):

	player_info = models.ForeignKey('PlayerInfo')

	is_completed = models.BooleanField(default=False)

	difficulty = models.CharField(max_length=16, choices=Article.DIFFICULTIES)
	max_stories = models.IntegerField(default=10)

	feedback_version = models.CharField(max_length=16, choices=(('friendly', 'friendly'), ('snarky', 'snarky'),), default='friendly')
	scoring_version = models.IntegerField(default=1)

	created_time = models.DateTimeField(auto_now_add=True)
	modified_time = models.DateTimeField(auto_now=True)

	current_round = models.ForeignKey('GameRound', null=True, blank=True)

	# mostly to support initial set up where game rounds are fixed...
	current_round_index = models.IntegerField(default=0, editable=False)
	game_round_list = models.TextField(default='[]')

	def started_articles(self):
		pass

	def start_new_round(self):
		pass

	def end_round(self, user_guess):
		pass

	def __unicode__(self):
		return 'Gameid '+str(self.pk)+': '+self.player_info.username + ' [' + ('completed' if self.is_completed else 'in play') + ']'

class GameRound(models.Model):

	player_info = models.ForeignKey('PlayerInfo')
	game_info = models.ForeignKey('GameInfo')

	article = models.ForeignKey(Article)

	start_time = models.DateTimeField(auto_now_add=True)
	end_time = models.DateTimeField(auto_now=True)

	is_completed = models.BooleanField(default=False)

	chunk2_requested = models.BooleanField(default=False)
	chunk3_requested = models.BooleanField(default=False)
	show_info_requested = models.BooleanField(default=False)

	player_guess = models.CharField(max_length=16, default='', blank=True)

	def __unicode__(self):
		return self.game_info.__unicode__()+ ' [round ' + ('completed' if self.is_completed else 'in play') + '] '+self.article.__unicode__()

class GameRoundList(models.Model):

	GAME_DIFFICULTIES = tuple((x,x) for x in ("easy", "medium", "hard"))

	game_round_list = models.TextField(default='[]')
	game_number = models.IntegerField(default=1)
	game_type = models.CharField(max_length=16, choices=GAME_DIFFICULTIES, default='easy')


