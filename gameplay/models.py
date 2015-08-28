import random
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
	news_source = models.CharField(max_length=36, default='', blank=True)

	# adminn-ing
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	has_completed_survey = models.BooleanField(default=False)

	current_game = models.ForeignKey('GameInfo', null=True, blank=True)

	def begin_new_game(self, difficulty="easy", max_rounds=10, feedback_version="snarky", scoring_version=1):

		self.end_current_game()

		new_game = GameInfo(player_info=self, difficulty=difficulty, max_rounds=max_rounds, feedback_version=feedback_version, scoring_version=scoring_version)
		new_game.save()

		self.current_game = new_game
		self.save()

	def get_random_unplayed_article(self, difficulty=None, exclude_articles=None):
		count = Article.objects.all().count()
		return Article.objects.get(pk=random.randint(1, count))

	def end_current_game(self):

		if self.current_game is None:
			return None

		g = self.current_game

		game_is_being_cancelled = False

		if g.current_round and not self.current_game.current_round.is_completed:
			game_is_being_cancelled = True
			g.end_round('cancel')

		num_current_rounds = GameRound.objects.filter(game_info=g).count()
		if num_current_rounds < g.max_rounds:
			game_is_being_cancelled = True

		if game_is_being_cancelled:
			g.was_cancelled = True

		g.is_completed = True

		if not game_is_being_cancelled:
			g.total_score += g.end_of_game_bonus()

		g.save()

		self.current_game = None
		self.save()

		return g


	def __unicode__(self):
		return self.username

class GameInfo(models.Model):

	player_info = models.ForeignKey('PlayerInfo', related_name='game_infos')

	is_completed = models.BooleanField(default=False)

	was_cancelled = models.BooleanField(default=False)

	difficulty = models.CharField(max_length=16, choices=Article.DIFFICULTIES)
	max_rounds = models.IntegerField(default=10)

	max_time = models.IntegerField(default=3*60)

	feedback_version = models.CharField(max_length=16, choices=(('friendly', 'friendly'), ('snarky', 'snarky'),), default='friendly')
	scoring_version = models.IntegerField(default=1)

	created_time = models.DateTimeField(auto_now_add=True)
	modified_time = models.DateTimeField(auto_now=True)

	current_round = models.ForeignKey('GameRound', null=True, blank=True)

	# mostly to support initial set up where game rounds are fixed...
	current_round_index = models.IntegerField(default=0, editable=False)
	game_round_list = models.TextField(default='[]')

	total_score = models.IntegerField(default=0)

	max_passes = models.IntegerField(default=3)
	total_passes = models.IntegerField(default=0)

	@property
	def total_time(self):
		return sum(int(r.duration) for r in GameRound.objects.filter(game_info=self, is_completed=True))

	def started_articles(self):
		pass

	def start_new_round(self):
		new_article = self.player_info.get_random_unplayed_article()
		new_round = GameRound(player_info=self.player_info, game_info=self, article=new_article)
		new_round.potential_score = self.score_round(new_round, assume_correct=True)
		new_round.save()

		self.current_round = new_round
		self.current_round_index = GameRound.objects.filter(game_info=self).count()
		self.save()

		return new_round

	def end_round(self, player_guess):
		self.current_round.player_guess = player_guess
		self.current_round.is_completed = True
		self.current_round.guess_correct = (self.current_round.article.article_type==self.current_round.player_guess)
		round_score = self.score_round()
		self.current_round.actual_score = round_score
		self.current_round.save()

		round_status = {'guess': player_guess, 'correct_answer': self.current_round.article.article_type, 'round_score': round_score, }

		if player_guess=='pass':
			self.total_passes += 1
		self.current_round = None
		self.total_score += round_score
		self.save()

		return round_status

	def score_round(self, round=None, assume_correct=False):
		if round is None:
			round = self.current_round
		if assume_correct or round.article.article_type==round.player_guess:
			round_score = 40
			if round.chunk2_requested:
				round_score -= 0
			if round.chunk3_requested:
				round_score -= 0
			if round.show_info_requested:
				round_score -= 0
		elif round.player_guess=="cancel":
			round_score = 0
		elif round.player_guess=="pass":
			if self.total_passes<self.max_passes:
				round_score = 0
			else:
				round_score = -5
		else:
			round_score = -10
		return round_score

	def end_of_game_bonus(self):
		bonus = 0
		if self.max_time > self.total_time:
			bonus += 20
		return bonus			

	def __unicode__(self):
		return 'Gameid '+str(self.pk)+': '+self.player_info.username + ' [' + ('cancelled' if self.was_cancelled else ('completed' if self.is_completed else 'in play')) + ']'

class GameRound(models.Model):

	player_info = models.ForeignKey('PlayerInfo')
	game_info = models.ForeignKey('GameInfo', related_name='game_rounds')

	article = models.ForeignKey(Article)

	start_time = models.DateTimeField(auto_now_add=True)
	end_time = models.DateTimeField(auto_now=True)

	is_completed = models.BooleanField(default=False)

	chunk2_requested = models.BooleanField(default=False)
	chunk3_requested = models.BooleanField(default=False)
	show_info_requested = models.BooleanField(default=False)

	player_guess = models.CharField(max_length=16, default='', blank=True)
	guess_correct = models.BooleanField(default=False)

	potential_score = models.IntegerField(default=30)
	actual_score = models.IntegerField(default=30)

	@property
	def duration(self):
		return (self.end_time-self.start_time).total_seconds()

	def __unicode__(self):
		return self.game_info.__unicode__()+ ' [round ' + ('completed' if self.is_completed else 'in play') + '] '+self.article.__unicode__()

class GameRoundList(models.Model):

	GAME_DIFFICULTIES = tuple((x,x) for x in ("easy", "medium", "hard"))

	game_round_list = models.TextField(default='[]')
	game_number = models.IntegerField(default=1)
	game_type = models.CharField(max_length=16, choices=GAME_DIFFICULTIES, default='easy')


