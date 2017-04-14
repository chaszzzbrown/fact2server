from django.contrib import admin
from . models import PlayerInfo, GamePlay, ArticlePlay, GameSettings

admin.site.register(PlayerInfo)

admin.site.register(GameSettings)

admin.site.register(GamePlay)
admin.site.register(ArticlePlay)
