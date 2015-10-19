import random
from django.db import models
from django.db.models import Avg, Sum, Count

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

	def begin_new_game(self, difficulty="easy", max_rounds=10, feedback_version="friendly", game_category="dev", game_settings=None):

		self.end_current_game()


		if game_settings is None:
			new_game = GameInfo(player_info=self, difficulty=difficulty, max_rounds=max_rounds, feedback_version=feedback_version)
		else:
			new_game = GameInfo.create_from_game_settings(game_settings)

		new_game.feedback_version = feedback_version
		new_game.game_category = game_category
		new_game.player_info=self
		new_game.save()

		self.current_game = new_game
		self.save()

	def get_random_unplayed_article(self, difficulty=None, exclude_articles=None):

		used_articles = [r.article.pk for r in GameRound.objects.filter(game_info=self.current_game)]

		available_articles = list(Article.objects.all().exclude(pk__in=used_articles))

		return random.choice(available_articles)

		# count = Article.objects.all().count()
		# return Article.objects.get(pk=random.randint(1, count))

	def end_current_game(self, tot_time=None):

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

		g.game_bonus = g.end_of_game_bonus(tot_time) 

		g.total_score += g.game_bonus

		g.is_completed = True

		g.got_bonus = g.game_bonus>0
		g.actual_time = g.total_time

		g.save()

		self.current_game = None
		self.save()

		return g


	def __unicode__(self):
		return self.username

class GameSettings(models.Model):

	name = models.CharField(max_length=16, default="easy_std")

	difficulty = models.CharField(max_length=16, choices=Article.DIFFICULTIES)

	max_rounds = models.IntegerField(default=10)
	max_time = models.IntegerField(default=3*60)
	max_passes = models.IntegerField(default=3)

	correct_article_score = models.IntegerField(default=40)
	incorrect_article_penalty = models.IntegerField(default=10)
	hint_penalty = models.IntegerField(default=5)

	time_bonus = models.IntegerField(default=20)

	low_score_threshold = models.IntegerField(default=10)
	medium_score_threshold = models.IntegerField(default=200)

	game_round_list = models.TextField(default='', blank=True)

	created_time = models.DateTimeField(auto_now_add=True)
	modified_time = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name+'['+self.difficulty+']'

class GameInfo(models.Model):

	player_info = models.ForeignKey('PlayerInfo', related_name='game_infos')

	is_completed = models.BooleanField(default=False)

	was_cancelled = models.BooleanField(default=False)

	game_category = models.CharField(max_length=16, default="dev")

	game_settings = models.ForeignKey('GameSettings', default=None, blank=True, null=True)

	difficulty = models.CharField(max_length=16, choices=Article.DIFFICULTIES)
	max_rounds = models.IntegerField(default=10)

	max_time = models.IntegerField(default=1*20)

	feedback_version = models.CharField(max_length=16, choices=(('friendly', 'friendly'), ('snarky', 'snarky'),), default='friendly')
	scoring_version = models.IntegerField(default=1)

	low_score_threshold = models.IntegerField(default=10)
	medium_score_threshold = models.IntegerField(default=200)

	created_time = models.DateTimeField(auto_now_add=True)
	modified_time = models.DateTimeField(auto_now=True)

	current_round = models.ForeignKey('GameRound', null=True, blank=True)

	# mostly to support initial set up where game rounds are fixed...
	current_round_index = models.IntegerField(default=0, editable=False)
	game_round_list = models.TextField(default='')

	total_score = models.IntegerField(default=0)

	game_bonus = models.IntegerField(default=0)

	max_passes = models.IntegerField(default=3)
	total_passes = models.IntegerField(default=0)

	got_bonus = models.BooleanField(default=False)
	actual_time = models.IntegerField(default=0)

	@staticmethod
	def fixupfields():
		for g in GameInfo.objects.all():
			g.got_bonus = g.game_bonus>0
			g.actual_time = min(g.total_time, g.max_time)
			g.save()

	@staticmethod
	def create_from_game_settings(game_settings_name):
		game_settings = GameSettings.objects.get(name=game_settings_name)
		g = GameInfo(game_settings=game_settings, 
						difficulty=game_settings.difficulty,
						max_rounds=game_settings.max_rounds,
						max_time=game_settings.max_time,
						max_passes=game_settings.max_passes,
						game_round_list=game_settings.game_round_list,

						low_score_threshold=game_settings.low_score_threshold,
						medium_score_threshold=game_settings.medium_score_threshold
						)
		return g

	@staticmethod
	def get_stats_for(game_category):
		stats = GameInfo.objects.filter(game_category=game_category, is_completed=True)
		stats = stats.values('game_settings__name', 'difficulty')
		stats = stats.annotate(average_score=Avg('total_score'), total_bonus_achieved=Sum('got_bonus'), average_time= Avg('actual_time'), average_bonus=Avg('game_bonus'), average_passes=Avg('total_passes'), total_played=Count('pk'))
		return list(stats)

	@property
	def hint_penalty(self):
		if (self.game_settings):
			return self.game_settings.hint_penalty
		else:
			return 0

	@property
	def total_time(self):
		return min(sum(int(r.duration) for r in GameRound.objects.filter(game_info=self, is_completed=True)) + 1, self.max_time)

	@property
	def game_round_pks(self):
		if self.game_round_list=='':
			return []
		else:
			return [int(pk.replace('A','')) for pk in (self.game_round_list.replace('(', '').replace(')','').replace('[','').replace(']','')).split(',')]

	@property
	def settings_name(self):
		if self.game_settings:
			return self.game_settings.name
		else:
			return 'default:'+self.difficulty

	def started_articles(self):
		pass

	def start_new_round(self):
		if self.current_round_index >= len(self.game_round_pks):
			new_article = self.player_info.get_random_unplayed_article()
		else:
			new_article = Article.objects.get(pk=self.game_round_pks[self.current_round_index])

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
		if self.game_settings:

			if assume_correct or round.article.article_type==round.player_guess:
				round_score = self.game_settings.correct_article_score
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
				round_score = - self.game_settings.incorrect_article_penalty

			if round.show_info_requested:
				round_score -= self.game_settings.hint_penalty

		else:

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

	def end_of_game_bonus(self, tot_time=None):
		bonus = 0
		print 'Calc bonus', tot_time, self.total_time
		if tot_time is None:
			tot_time = self.total_time

		if tot_time < self.max_time: # or self.current_round_index>=self.max_rounds:
			if self.game_settings:
				bonus += self.game_settings.time_bonus
			else:
				bonus += 20
		print "Bonus: %d, %d, %d, %d, %d" % (bonus, self.max_time, tot_time, self.current_round_index, self.max_rounds)
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

	@staticmethod
	def get_stats_for(game_category):
		stats = GameRound.objects.filter(game_info__game_category=game_category, is_completed=True).exclude(player_guess='cancel')
		stats = stats.values('article__pk', 'article__article_type', 'article__headline', 'article__difficulty')
		stats = stats.annotate(total_correct=Sum('guess_correct'),total_viewed=Count('pk'), average_correct=Avg('guess_correct'))
		return list(stats)

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


