from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status

from gameplay.models import PlayerInfo
from gameplay.serializers import PlayerInfoSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def player_info(request, pk=None):

	if request.Method=='GET':
		if pk is None:
			try:
				p = PlayerInfo.objects.get(user_name=request.GET['user_name'])
			except KeyError:
				return HttpResponse('no user_name specified', status=status.HTTP_400_BAD_REQUEST)
			except PlayerInfo.DoesNotExist:
				return HttpResponse('not found', status=status.HTTP_404_NOT_FOUND)
		else:
			try:
				p = PlayerInfo.objects.get(pk=pk)
			except PlayerInfo.DoesNotExist:
				return HttpResponse('not found', status=status.HTTP_404_NOT_FOUND)

		serializer = PlayerInfoSerializer(p)
		return JSONResponse(serializer.data, status=status.HTTP_200_OK)

		

