from my_app.models import PlayerSkill
from rest_framework import serializers

from ..models.player import Player
from .player_skill import PlayerSkillSerializer
from rest_framework.exceptions import ValidationError


class PlayerSerializer(serializers.ModelSerializer):
    playerSkills = PlayerSkillSerializer(many=True)

    class Meta:
        model = Player
        fields = ['id', 'name', 'position', 'playerSkills']

    
    
    def validate(self, attrs):
        validated_data = super().validate(attrs)

        # Check position field
        position = validated_data.get('position')
        if position not in ['defender', 'midfielder', 'forward']:
            error_message = "Invalid value for position: {}".format(position)
            raise serializers.ValidationError({"message": error_message})

        # Check playerSkills field
        player_skills = validated_data.get('playerSkills')
        valid_skills = ['defense', 'attack', 'speed', 'strength', 'stamina']
        for skill in player_skills:
            skill_name = skill.get('skill')
            if skill_name not in valid_skills:
                error_message = "Invalid skill: {}".format(skill_name)
                raise serializers.ValidationError({"message": error_message})
        return validated_data
    
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
    


