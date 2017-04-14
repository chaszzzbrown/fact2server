from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed

import json

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from gameplay2.models import *
from gameplay2.serializers import *

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = json.dumps(data) # JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@api_view(['GET', 'POST'])
def player_info(request, pk=None):
	if request.method=='GET':
		if pk is None:
			try:
				username = request.GET['username']
			except (KeyError, ValueError,):
				return HttpResponse('no username specified', status=status.HTTP_400_BAD_REQUEST)

			try:
				p = PlayerInfo.objects.get(username=username)
			except PlayerInfo.DoesNotExist:
				return HttpResponse('not found', status=status.HTTP_404_NOT_FOUND)
		else:
			try:
				p = PlayerInfo.objects.get(pk=pk)
			except PlayerInfo.DoesNotExist:
				return HttpResponse('not found', status=status.HTTP_404_NOT_FOUND)

		serializer = PlayerInfoSerializer(p)
		return JSONResponse(serializer.data, status=status.HTTP_200_OK)

	elif request.method=='POST':
		return HttpResponse('POST not implemented yet', status=status.HTTP_400_BAD_REQUEST)
	else:
		return HttpResponse('Only GET or POST are accepted', status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def player_begin_game(request, pk, do_create=True):

	# enforce POST method

	# validate player
	try:
		p = PlayerInfo.objects.get(pk=pk)
	except PlayerInfo.DoesNotExist:
		return HttpResponse('not found', status=status.HTTP_404_NOT_FOUND)

	# if existing game, then cancel it
	if p.current_game:
		p.current_game.was_cancelled = True
		p.current_game.save()

	game_settings, created = GameSettings.objects.get_or_create()
	gs_data = json.loads(game_settings.game_settings_json)

	# construct new game
	if do_create:
		new_game = GamePlay.objects.create(player_info=p, game_settings_json=game_settings.game_settings_json)
	else:
		new_game = GamePlay(player_info=p, game_settings_json=game_settings.game_settings_json)

	new_game.maximum_score = gs_data['maximum_score']
	new_game.maximum_articles_played = gs_data['maximum_articles_played']
	new_game.game_state = {}

	if do_create:
		new_game.save()
		p.current_game = new_game
		p.save()

	g_serializer = GamePlaySerializer(new_game)

	# return it
	return JSONResponse(g_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def player_begin_unsaved_game(request, pk):
	return player_begin_game(request, pk, False)

def player_end_game(request,pk):
	pass

@api_view(['GET', 'POST'])
def game_play(request, pk):
	try:
		g = GamePlay.objects.get(pk=pk)
	except GamePlay.DoesNotExist:
		return HttpResponse('not found', status=status.HTTP_404_NOT_FOUND)
	
	if request.method=='GET':
		g_serializer = GamePlaySerializer(g)
		return JSONResponse(g_serializer.data, status=status.HTTP_200_OK)
	elif request.method=='POST':
		g_serializer = GamePlaySerializer(g, data=request.data, partial=True)
		print request.data['game_state']
		if g_serializer.is_valid():
			g.game_state = request.data['game_state']
			g_serializer.save()
			return JSONResponse(g_serializer.data, status=status.HTTP_200_OK)
		else:
			return HttpResponse('POST was not valid', status=status.HTTP_400_BAD_REQUEST)
	else:
		return HttpResponse('Only GET and POST are supported', status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
# @permission_classes((AllowAny, ))
def game_settings(request):

	if request.method=="GET":
		settings, created = GameSettings.objects.get_or_create()
		res = json.loads(settings.game_settings_json)
		res['modified_date'] = settings.modified_date.isoformat()
		return JSONResponse(res, status=status.HTTP_200_OK)
	elif request.method=='POST':
		res = request.data

		if 'modified_date' in res:
			del res['modified_date']

		settings, created = GameSettings.objects.get_or_create()
		settings.game_settings_json = json.dumps(res)
		settings.save()

		res['modified_date'] = settings.modified_date.isoformat()
		return JSONResponse(res, status=status.HTTP_200_OK)

	else:
		return HttpResponse('Only GET and POST are supported', status=status.HTTP_400_BAD_REQUEST)
