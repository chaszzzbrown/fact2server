import json

from django.shortcuts import render

from django.db import IntegrityError
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status

from gameplay.models import PlayerInfo, GameInfo, GameRound
from gameplay.serializers import PlayerInfoSerializer, GameInfoSerializer, GameRoundSerializer, GameRoundStatusSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = json.dumps(data) # JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
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

	elif request.method=='PUT':
		try:
			p = PlayerInfo.objects.get(pk=pk)
		except PlayerInfo.DoesNotExist:
			return HttpResponse('not found', status=status.HTTP_404_NOT_FOUND)

		try:
			data = json.loads(request.body)
		except ValueError:
			return HttpResponse('bad json', status=status.HTTP_400_BAD_REQUEST)

		serializer = PlayerInfoSerializer(p, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=status.HTTP_200_OK)
		
		return HttpResponse('cannot post', status=status.HTTP_400_BAD_REQUEST)

	elif request.method=='POST':
		if pk is not None:
			return HttpResponse('cannot post to existing pk', status=status.HTTP_400_BAD_REQUEST)

		try:
			data = json.loads(request.body)
		except ValueError:
			return HttpResponse('bad json', status=status.HTTP_400_BAD_REQUEST)

		if 'username' not in data or data['username']=='':
			return HttpResponse('must supply valid username', status=status.HTTP_400_BAD_REQUEST)

		try:
			p = PlayerInfo(username=data['username'])
			p.save()
		except IntegrityError:
			return HttpResponse('username already in use', status=status.HTTP_400_BAD_REQUEST)

		serializer = PlayerInfoSerializer(p)
		return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)

@csrf_exempt
def player_begin_game(request, pk):
	if request.method=='POST':
		try:
			p = PlayerInfo.objects.get(pk=pk)
		except PlayerInfo.DoesNotExist:
			return HttpResponse('not found', status=status.HTTP_404_NOT_FOUND)

		p.begin_new_game()

		serp = PlayerInfoSerializer(p)
		serg = GameInfoSerializer(p.current_game)
		data = {'player_info': serp.data, 'game_info':serg.data}
		return JSONResponse(data, status=status.HTTP_201_CREATED)
	else:
		return HttpResponse('must use POST', status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def player_end_game(request, pk):
	if request.method=='POST':
		try:
			p = PlayerInfo.objects.get(pk=pk)
		except PlayerInfo.DoesNotExist:
			return HttpResponse('not found', status=status.HTTP_404_NOT_FOUND)

		data = json.loads(request.body)
		tot_time = data.get('tot_time', None)
		ended_game = p.end_current_game(tot_time)

		serp = PlayerInfoSerializer(p)
		serg = GameInfoSerializer(ended_game) 
		data = {'player_info': serp.data, 'game_info': serg.data if ended_game else None}
		return JSONResponse(data, status=status.HTTP_200_OK)
	else:
		return HttpResponse('must use POST', status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def game_info(request, pk):

	if request.method=='GET':
		try:
			g = GameInfo.objects.get(pk=pk)
		except GameInfo.DoesNotExist:
			return HttpResponse('not found', status=status.HTTP_404_NOT_FOUND)

		serializer = GameInfoSerializer(g)
		return JSONResponse(serializer.data, status=status.HTTP_200_OK)

	else:
		return HttpResponse('not permitted', status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def game_end_round(request, pk):

	if request.method != 'POST':
		return HttpResponse('must use POST', status=status.HTTP_400_BAD_REQUEST)

	try:
		g = GameInfo.objects.get(pk=pk)

	except GameInfo.DoesNotExist:
		return HttpResponse('game not found', status=status.HTTP_404_NOT_FOUND)

	if g.current_round is None:
		return HttpResponse('no current round', status=status.HTTP_400_BAD_REQUEST)

	if g.current_round.is_completed:
		return HttpResponse('current round is already complete', status=status.HTTP_400_BAD_REQUEST)

	try:
		guess = json.loads(request.body)['guess']
	except (ValueError, KeyError):
		return HttpResponse('missing guess parameter', status=status.HTTP_400_BAD_REQUEST)

	round_status = g.end_round(guess)

	serializer = GameInfoSerializer(g)
	data = serializer.data

	res = {'round_status': round_status, 'game_info': data}

	return JSONResponse(res, status=status.HTTP_200_OK)

@csrf_exempt
def game_start_round(request, pk):
	try:
		g = GameInfo.objects.get(pk=pk)

	except GameInfo.DoesNotExist:
		return HttpResponse('game not found', status=status.HTTP_404_NOT_FOUND)

	if g.current_round and not g.current_round.is_completed:
		return HttpResponse('current round is not completed', status=status.HTTP_400_BAD_REQUEST)

	new_round = g.start_new_round()

	serializer = GameRoundSerializer(new_round)

	data = serializer.data
	data['article'] = new_round.article.forJSON()

	res = {'game_info': GameInfoSerializer(g).data, 'new_round': data}

	return JSONResponse(res, status=status.HTTP_200_OK)

@csrf_exempt
def game_round_info(request, pk):
	return game_round_full_info(request, pk, full_info=False)

@csrf_exempt
def game_round_full_info(request, pk, full_info=True):

	try:
		gr = GameRound.objects.get(pk=pk)
	except GameRound.DoesNotExist:
		return HttpResponse('not found', status=status.HTTP_404_NOT_FOUND)

	if request.method=='GET':
		serializer = GameRoundSerializer(gr)

		data = serializer.data
		if full_info and gr:
			data['article'] = gr.article.forJSON()

		return JSONResponse(data, status=status.HTTP_200_OK)

	elif request.method=='POST':
		try:
			data = json.loads(request.body)
		except ValueError:
			return HttpResponse('bad json', status=status.HTTP_400_BAD_REQUEST)

		serializer = GameRoundStatusSerializer(gr, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			gr.potential_score = gr.game_info.score_round(gr, assume_correct=True)
			gr.save()

			serializer = GameRoundSerializer(gr)

			data = serializer.data
			if full_info and gr:
				data['article'] = gr.article.forJSON()

			return JSONResponse(data, status=status.HTTP_200_OK)

		else:
			return HttpResponse('invalid parameters', status=status.HTTP_400_BAD_REQUEST)

	else:
		return HttpResponse('not permitted', status=status.HTTP_400_BAD_REQUEST)



