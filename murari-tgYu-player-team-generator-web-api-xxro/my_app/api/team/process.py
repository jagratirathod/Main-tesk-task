## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from rest_framework.request import Request
from rest_framework import status
from my_app.models import Player
from my_app.serializers.player import PlayerSerializer
from django.db.models import Max

from my_app.serializers.team import TeamSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

def team_process_handler(request: Request):
    serializer = TeamSerializer(data=request.data, many=True, context={'unique_combinations': []})
    if not serializer.is_valid():
        raise ValidationError(serializer.errors[1]["message"][0])
    team_requirements = serializer.validated_data

    selected_players = []

    for requirement in team_requirements:
        position = requirement.get('position')
        main_skill = requirement.get('mainSkill')
        num_players = requirement.get('numberOfPlayers')

        players = Player.objects.filter(playerSkills__skill=main_skill, position=position).distinct()
        selected_players.extend(players.order_by('-playerSkills__value')[:num_players])

    serializer = PlayerSerializer(selected_players, many=True)
    serialized_data = serializer.data

    return Response(serialized_data, status=status.HTTP_200_OK)


        









