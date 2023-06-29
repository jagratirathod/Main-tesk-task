# /////////////////////////////////////////////////////////////////////////////
# YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
# /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from my_app.serializers.player import PlayerSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response


def create_player_handler(request: Request):
    serializer = PlayerSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
    # else:
    #     message = f"Invalid value for position: {request.data['position']}"
    #     return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)

