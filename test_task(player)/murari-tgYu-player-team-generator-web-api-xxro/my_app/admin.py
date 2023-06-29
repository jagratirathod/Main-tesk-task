from django.contrib import admin
from my_app.models import Player, PlayerSkill


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'position']


admin.site.register(Player, PlayerAdmin)


class PlayerSkillAdmin(admin.ModelAdmin):
    list_display = ['id', 'player', 'skill', 'value']


admin.site.register(PlayerSkill, PlayerSkillAdmin)
