## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from my_app.models import Player
from my_app.serializers.player import PlayerSerializer
from django.db.models import Max


def team_process_handler(request):
    team_requirements = request.data
    
    selected_players = []
    unique_combinations = []

    for requirement in team_requirements:
        position = requirement.get('position')
        main_skill = requirement.get('mainSkill')
        num_players = requirement.get('numberOfPlayers')

        combination = (position, main_skill)
        if combination in unique_combinations:
            message = f"Duplicate combination of position: {position} and mainSkill: {main_skill}"
            return JsonResponse({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        unique_combinations.append(combination)

        if  Player.objects.filter(position=position):
            players = Player.objects.filter(playerSkills__skill=main_skill, position=position).distinct()
            
            if len(players) >= num_players:
                players = players.order_by('-playerSkills__value')[:num_players]
            else:
                players = Player.objects.annotate(max_value=Max('playerSkills__value')).order_by('-max_value')[:num_players]
                if len(players) < num_players:
                    message = f"Insufficient number of players for position: {position}"
                    return JsonResponse({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = f"Insufficient number of players for position: {position}"
            return JsonResponse({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        
        selected_players.extend(players)

    serializer = PlayerSerializer(selected_players, many=True)
    serialized_data = serializer.data

    return JsonResponse(serialized_data, status=status.HTTP_200_OK, safe=False)




        









