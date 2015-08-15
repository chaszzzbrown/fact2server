from django.forms import widgets

from rest_framework import serializers
from gameplay.models import PlayerInfo, GameInfo, GameRound

class GameRoundSerializer(serializers.ModelSerializer):

	class Meta:
		model = GameRound
		fields = ('is_completed', 'player_info', 'game_info', 'article', 'start_time', 'end_time', 
					'is_completed', 'chunk2_requested', 'chunk3_requested', 'show_info_requested', 'player_guess')

class GameInfoSerializer(serializers.ModelSerializer):

	rounds = GameRoundSerializer(many=True, read_only=True)

	class Meta:
		model = GameInfo
		fields = ('pk', 'player_info', 'is_completed', 'difficulty', 'max_stories', 'feedback_version', 'scoring_version', 
					'created_time', 'modified_time', 'current_round', 'current_round_index', 'game_round_list', 'rounds',)

class PlayerInfoSerializer(serializers.ModelSerializer):
	game_infos = GameInfoSerializer(many=True, read_only=True)

	class Meta:
		model = PlayerInfo
		fields = ('pk', 'username', 'age', 'gender', 'education', 'computer_use', 'news_media_savvy', 'news_source', 'current_game', 'game_infos',)


