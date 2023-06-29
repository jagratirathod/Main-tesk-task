from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class GymEquipment(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name}"


class Exercise(models.Model):
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    gym_equipment = models.ForeignKey(GymEquipment, on_delete=models.CASCADE) 
    duration =  models.PositiveIntegerField(help_text="Please add duration in minutes.")
    description = models.CharField(max_length=100, null=True, blank=True)
    calories_burnt = models.PositiveIntegerField()
    created_at = models.DateField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.athlete}"