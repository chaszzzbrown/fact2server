from django.db.models import Count, Sum, Avg, F, Q
from django.utils import timezone
import datetime

from . models import *

def articlePlayStats(start_date, end_date, articleList=None):
	stats = Article.objects

	# optional filter(s) on ArticlePlays; e.g.
	# stats = stats.filter(articleplay__showed_hint=True)
	if start_date:
		start_date = datetime.datetime(start_date.year, start_date.month, start_date.day)
		if end_date:
			end_date = datetime.datetime(end_date.year, end_date.month, end_date.day)+datetime.timedelta(days=1)
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

	print by_outcome
	return by_outcome


