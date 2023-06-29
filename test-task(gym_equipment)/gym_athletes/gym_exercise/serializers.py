from rest_framework import serializers
from . models import Exercise


class ExerciseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['gym_equipment','duration','description','calories_burnt']




