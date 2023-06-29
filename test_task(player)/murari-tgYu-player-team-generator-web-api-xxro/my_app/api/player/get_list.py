# /////////////////////////////////////////////////////////////////////////////
# YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
# /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from my_app.models import Player
from my_app.serializers.player import PlayerSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response




def get_player_list_handler(request):
    players = Player.objects.all()
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)
