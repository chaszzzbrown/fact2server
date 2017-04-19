from django.db.models import Count, Sum, Avg, F
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
	stats = GamePlay.objects

	# optional filter(s) on ArticlePlays; e.g.
	# stats = stats.filter(articleplay__showed_hint=True)
	if start_date:
		start_date = datetime.datetime(start_date.year, start_date.month, start_date.day)
		if end_date:
			end_date = datetime.datetime(end_date.year, end_date.month, end_date.day)+datetime.timedelta(days=1)
			stats = stats.filter(created_date__gte=start_date, created_date__lte=end_date)
		else:
			stats = stats.filter(created_date__gte=start_date)


	stats = stats.values('is_completed', 'was_cancelled').annotate(
				num_plays=Count('pk'), 
				avg_time=Avg('total_time_seconds'), 
				avg_completed=Avg('total_articles_played'),
				avg_pct_completed=Avg(F('total_articles_played')*1.0/F('maximum_articles_played')),
				avg_correct=Avg('total_articles_correct'),
				avg_pct_correct=Avg(F('total_articles_correct')*1.0/F('maximum_articles_played')),
				avg_score=Avg('total_score'),
				avg_pct_score=Avg(F('total_score')*1.0/F('maximum_score')),
			)

	return stats


