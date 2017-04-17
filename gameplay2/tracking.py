from django.db.models import Count, Sum, Avg

from . models import *

def articlePlayStats(articleList=None):
	stats = Article.objects

	# optional filter(s) on ArticlePlays; e.g.
	# stats = stats.filter(articleplay__showed_hint=True)

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

def articlePlayStatsForDisplay(articleList=None):
	stats = list(articlePlayStats(articleList).order_by('-pk').filter(num_plays__gt=0))

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


def gamePlayStats():
	stats = GamePlay.objects

	# optional filter(s) on ArticlePlays; e.g.
	# stats = stats.filter(articleplay__showed_hint=True)

