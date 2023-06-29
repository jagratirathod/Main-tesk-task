# /////////////////////////////////////////////////////////////////////////////
# YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
# /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from my_app.serializers.player import PlayerSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


def create_player_handler(request: Request):
    serializer = PlayerSerializer(data=request.data)
    if not serializer.is_valid():
        raise ValidationError({"messsge": serializer.errors["message"][0]})
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    
