# /////////////////////////////////////////////////////////////////////////////
# YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
# /////////////////////////////////////////////////////////////////////////////

from typing import Any

from django.http.response import JsonResponse
from my_app.models.player import Player
from my_app.serializers.player import PlayerSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, ValidationError



def update_player_handler(request: Request, id: Any):
    try:
        player = Player.objects.get(id=id)
        serializer = PlayerSerializer(player, data=request.data, partial=True)
        if not serializer.is_valid():
            raise ValidationError({"messsge": serializer.errors["message"][0]})
        serializer.save()
        return Response(serializer.data)
    except ObjectDoesNotExist:
        raise NotFound("Player not found")

