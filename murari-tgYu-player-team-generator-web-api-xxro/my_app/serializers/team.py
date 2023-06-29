from my_app.models import Player
from rest_framework import serializers

class TeamSerializer(serializers.Serializer):
    position = serializers.CharField()
    mainSkill = serializers.CharField()
    numberOfPlayers = serializers.IntegerField()

    def validate(self, attrs):
        position = attrs.get('position')
        main_skill = attrs.get('mainSkill')
        num_players = attrs.get('numberOfPlayers')

        # Check for duplicate combination
        existing_combinations = self.context.get('unique_combinations', [])
        combination = (position, main_skill)
        if combination in existing_combinations:
            raise serializers.ValidationError({"message":f"Duplicate combination of position: {position} and mainSkill: {main_skill}"})
        
        # Check for sufficient players
        players = Player.objects.filter(playerSkills__skill=main_skill, position=position).distinct()
        if not players.exists() or len(players) < num_players:
            raise serializers.ValidationError({"message":f"Insufficient number of players for position: {position}"})
        
        # Update unique combinations
        existing_combinations.append(combination)

        return attrs