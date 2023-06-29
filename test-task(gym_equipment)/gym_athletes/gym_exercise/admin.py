from django.contrib import admin
from . models import GymEquipment , Exercise


class GymEquipmentAdmin(admin.ModelAdmin):
    list_display = ['id','name']
admin.site.register(GymEquipment, GymEquipmentAdmin)


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['id','athlete','gym_equipment','duration','description','calories_burnt','created_at']
admin.site.register(Exercise, ExerciseAdmin)
