from django.contrib import admin
from . models import PlayerInfo, GameInfo, GameRound, GameRoundList

# Register your models here.
admin.site.register(PlayerInfo)


@admin.register(GameInfo)
class GameInfoAdmin(admin.ModelAdmin):
	readonly_fields = ('current_round_index', 'created_time', 'modified_time',)

admin.site.register(GameRound)
admin.site.register(GameRoundList)
