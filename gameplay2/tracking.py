from django.db.models import Count, Sum, Avg, F, Q
from django.utils import timezone
import datetime

from . models import *

def articlePlayStats(start_date, end_date, articleList=None):
	stats = Article.objects

	# optional filter(s) on ArticlePlays; e.g.
	# stats = stats.filter(articleplay__showed_hint=True)
	if start_date:
		start_date = timezone.make_aware(datetime.datetime(start_date.year, start_date.month, start_date.day))
		if end_date:
			end_date = timezone.make_aware(datetime.datetime(end_date.year, end_date.month, end_date.day)+datetime.timedelta(days=1))
			stats = stats.filter(articleplay__created_date__lte=end_date, articleplay__created_date__gte=start_date)
		else:
			stats = stats.filter(articleplay__created_date__gte=start_date)


	# perform the annotation
	stats= stats.annotate(	num_plays=Count('articleplay'), 
							num_correct=Sum('articleplay__was_correct'), 
							num_hints=Sum('articleplay__showed_hint'), 
							avg_time=Avg('articleplay__total_time_seconds'))

	# optional post filter on articles; e.g.:
	if articleList:
		stats = stats.filter(pk__in=articleList)

	stats.order_by('-pk')

	return stats

def articlePlayStatsForDisplay(start_date, end_date, articleList=None):

	stats = list(articlePlayStats(start_date, end_date, articleList=None).order_by('-pk').filter(num_plays__gt=0))

	allArticles = Article.objects.all()
	if articleList:
		allArticles = allArticles.filter(pk__in=articleList)

	allArticles = list(allArticles.order_by('-pk'))

	res = []
	for aa in allArticles:
		if len(stats)==0 or aa.pk > stats[0].pk:
			base_info = aa.forJSONList()
			base_info['num_plays'] = 0
			base_info['num_correct'] = 0
			base_info['num_hints'] = 0
			base_info['avg_time'] = 0
			res.append(base_info)
		else:
			sa = stats[0]
			base_info = sa.forJSONList()
			base_info['num_plays'] = sa.num_plays
			base_info['num_correct'] = sa.num_correct
			base_info['num_hints'] = sa.num_hints
			base_info['avg_time'] = sa.avg_time
			res.append(base_info)
			stats = stats[1:]

	return res


def gamePlayStats(start_date, end_date, articleList=None):

	def applyDateFilter(stats):
		if start_date:
			sd = timezone.make_aware(datetime.datetime(start_date.year, start_date.month, start_date.day))
			if end_date:
				ed = timezone.make_aware(datetime.datetime(end_date.year, end_date.month, end_date.day)+datetime.timedelta(days=1))
				return stats.filter(created_date__gte=sd, created_date__lte=ed)
			else:
				return stats.filter(created_date__gte=sd)

	# first do the "not potentially in play games..."

	stats = GamePlay.objects

	stats = applyDateFilter(stats)

	stats = stats.values('is_completed', 'was_cancelled').filter(Q(is_completed=True) | Q(was_cancelled=True)).annotate(
				num_plays=Count('pk'), 
				avg_time=Avg('total_time_seconds'), 
				avg_completed=Avg('total_articles_played'),
				avg_pct_completed=Avg(F('total_articles_played')*1.0/F('maximum_articles_played')),
				avg_correct=Avg('total_articles_correct'),
				avg_pct_correct=Avg(F('total_articles_correct')*1.0/F('maximum_articles_played')),
				avg_score=Avg('total_score'),
				avg_pct_score=Avg(F('total_score')*1.0/F('maximum_score')),
			)

	by_outcome = {}
	for row in list(stats):
		if row['is_completed']:
			by_outcome['completed'] = row
		elif row['was_cancelled']:
			by_outcome['cancelled'] = row

	# next the abndoned games...
	dt48Hours = timezone.make_aware(datetime.datetime.now() - datetime.timedelta(hours=8))

	stats = GamePlay.objects

	stats = applyDateFilter(stats)

	stats = stats.values('is_completed', 'was_cancelled').filter(Q(is_completed=False) & Q(was_cancelled=False) & Q(modified_date__lte=dt48Hours)).annotate(
				num_plays=Count('pk'), 
				avg_time=Avg('total_time_seconds'), 
				avg_completed=Avg('total_articles_played'),
				avg_pct_completed=Avg(F('total_articles_played')*1.0/F('maximum_articles_played')),
				avg_correct=Avg('total_articles_correct'),
				avg_pct_correct=Avg(F('total_articles_correct')*1.0/F('maximum_articles_played')),
				avg_score=Avg('total_score'),
				avg_pct_score=Avg(F('total_score')*1.0/F('maximum_score')),
			)

	for row in list(stats):
		by_outcome['abandoned'] = row

	# next the in play games...
	stats = GamePlay.objects

	stats = applyDateFilter(stats)

	stats = stats.values('is_completed', 'was_cancelled').filter(Q(is_completed=False) & Q(was_cancelled=False) & Q(modified_date__gte=dt48Hours)).annotate(
				num_plays=Count('pk'), 
				avg_time=Avg('total_time_seconds'), 
				avg_completed=Avg('total_articles_played'),
				avg_pct_completed=Avg(F('total_articles_played')*1.0/F('maximum_articles_played')),
				avg_correct=Avg('total_articles_correct'),
				avg_pct_correct=Avg(F('total_articles_correct')*1.0/F('maximum_articles_played')),
				avg_score=Avg('total_score'),
				avg_pct_score=Avg(F('total_score')*1.0/F('maximum_score')),
			)

	for row in list(stats):
		by_outcome['inPlay'] = row

	return by_outcome

def get_article_plays(start_date, end_date):
	rows = ArticlePlay.objects.all()

	# optional filter(s) on ArticlePlays; e.g.
	# stats = stats.filter(articleplay__showed_hint=True)
	if start_date:
		start_date = timezone.make_aware(datetime.datetime(start_date.year, start_date.month, start_date.day))
		if end_date:
			end_date = timezone.make_aware(datetime.datetime(end_date.year, end_date.month, end_date.day)+datetime.timedelta(days=1))
			rows = rows.filter(created_date__lte=end_date, created_date__gte=start_date)
		else:
			rows = rows.filter(created_date__gte=start_date)

	headers = ['pk', 'player_pk', 'article_id', 'date/time', 'total_seconds', 'was_correct', 'showed_hint']

	csv = ['\t'.join(headers)]

	for row in rows:
		next_row = [str(row.pk), str(row.player_info.pk), str(row.article.pk), 
						row.created_date.strftime('%m/%d/%Y %H:%M:%S'), 
						str(row.total_time_seconds), '1' if row.was_correct else '0', '1' if row.showed_hint else '0', ]
		csv.append('\t'.join(next_row))

	return '\n'.join(csv)

'''
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	player_info = models.ForeignKey('PlayerInfo', related_name='game_plays')

	game_settings_json = models.TextField(default='{}', blank=True)

	# these fields will be manually updated by the client side
	total_score = models.IntegerField(default=0)
	total_time_seconds = models.IntegerField(default=0)
	total_articles_played = models.IntegerField(default=0)
	total_articles_correct = models.IntegerField(default=0)

	maximum_score = models.IntegerField(default=0)
	maximum_articles_played = models.IntegerField(default=0)

	game_outcome
'''

def get_game_plays(start_date, end_date):
	rows = GamePlay.objects.all()

	# optional filter(s) on ArticlePlays; e.g.
	# stats = stats.filter(articleplay__showed_hint=True)
	if start_date:
		start_date = timezone.make_aware(datetime.datetime(start_date.year, start_date.month, start_date.day))
		if end_date:
			end_date = timezone.make_aware(datetime.datetime(end_date.year, end_date.month, end_date.day)+datetime.timedelta(days=1))
			rows = rows.filter(created_date__lte=end_date, created_date__gte=start_date)
		else:
			rows = rows.filter(created_date__gte=start_date)

	headers = ['pk', 'date/time', 'player_pk', 'outcome', 'total_seconds', 'total_score', 'maximum_score', 
					'articles_played', 'articles_correct', 'maximum_articles', 'game_state']

	csv = ['\t'.join(headers)]

	for row in rows:
		next_row = [str(row.pk), row.created_date.strftime('%m/%d/%Y %H:%M:%S'), str(row.player_info.pk), 
					row.game_outcome, str(row.total_time_seconds), str(row.total_score), str(row.maximum_score),
					str(row.total_articles_played), str(row.total_articles_correct), str(row.maximum_articles_played),
					str(row.game_state)]
		csv.append('\t'.join(next_row))

	return '\n'.join(csv)

'''
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

'''

def get_player_infos(start_date, end_date):
	rows = PlayerInfo.objects.all().filter(is_anonymous=False)

	# optional filter(s) on ArticlePlays; e.g.
	# stats = stats.filter(articleplay__showed_hint=True)
	if start_date:
		start_date = timezone.make_aware(datetime.datetime(start_date.year, start_date.month, start_date.day))
		if end_date:
			end_date = timezone.make_aware(datetime.datetime(end_date.year, end_date.month, end_date.day)+datetime.timedelta(days=1))
			rows = rows.filter(modified_date__lte=end_date, modified_date__gte=start_date)
		else:
			rows = rows.filter(modified_date__gte=start_date)

	headers = ['pk', 'created', 'last active', 'username', 'age', 'gender', 'education', 'media_savvy']

	csv = ['\t'.join(headers)]

	for row in rows:
		next_row = [str(row.pk), row.created_date.strftime('%m/%d/%Y %H:%M:%S'), row.modified_date.strftime('%m/%d/%Y %H:%M:%S'),  
					row.username, str(row.age), row.gender, row.education, str(row.news_media_savvy)]
		csv.append('\t'.join(next_row))

	return '\n'.join(csv)
