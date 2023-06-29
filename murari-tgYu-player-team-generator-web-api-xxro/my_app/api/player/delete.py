## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from typing import Any

from django.http.response import JsonResponse
from my_app.models import Player
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from functools import wraps


def is_token_valid(token):
    """
    function to match token
    """
    required_token="Bearer SkFabTZibXE1aE14ckpQUUxHc2dnQ2RzdlFRTTM2NFE2cGI4d3RQNjZmdEFITmdBQkE="
    return token==required_token.split(' ')[1]

def validate_token(func):
    """"
    decorator for validate token
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if 'Authorization' not in request.headers:
            return Response({'error': 'Missing Authorization header'}, status=status.HTTP_401_UNAUTHORIZED)

        # Extract the token from the header
        header = request.headers['Authorization']
        token = header.split(' ')[1] if len(header.split(' ')) > 1 else None
        
        if not is_token_valid(token):
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return func(request, *args, **kwargs)

    return wrapper



@validate_token
def delete_player_handler(request: Request, id: Any):
    try:
        player = Player.objects.get(id=id)
        player.delete()
        message = f"Player Deleted of position: {player.position}"
        return JsonResponse({"message": message}, status=status.HTTP_204_NO_CONTENT, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Player not found"}, status=status.HTTP_404_NOT_FOUND)


    
