from gameplay2.models import *

def fixPlayerInfo():
	for f in PlayerInfo.objects.all():
		if f.pk%10000==0:
			print f.pk
		try:
			g = f.current_game
		except:
			print f.pk, 'Exception'
			f.current_game = None
			f.save()

def checkGameInfo():
	for g in GamePlay.objects.all():
		if g.pk%10000==0:
			print g.pk
		try:
			p = g.player_info
		except:
			print g.pk, 'Exception'
