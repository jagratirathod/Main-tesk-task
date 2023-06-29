from my_app.models import PlayerSkill
from rest_framework import serializers

from ..models.player import Player
from .player_skill import PlayerSkillSerializer


class PlayerSerializer(serializers.ModelSerializer):
    playerSkills = PlayerSkillSerializer(many=True)

    class Meta:
        model = Player
        fields = ['id', 'name', 'position', 'playerSkills']

    # def validate_position(self, value):
    #     # Add your custom validation logic for the position field here
    #     if not value :
    #         raise serializers.ValidationError("Invalid value for position")
    #     return value


    def create(self, validated_data):
        skills_data = validated_data.pop('playerSkills')
        player = Player.objects.create(**validated_data)
        for skill_data in skills_data:
            PlayerSkill.objects.create(player=player, **skill_data)
        return player
    

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.position = validated_data.get('position', instance.position)
        instance.save()

        # Update player skills
        skills_data = validated_data.pop('playerSkills')

        for skill_data in skills_data:
          PlayerSkill.objects.create(player=instance, **skill_data)
        return instance
    


