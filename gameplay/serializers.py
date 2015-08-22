from django.forms import widgets

from rest_framework import serializers
from gameplay.models import PlayerInfo, GameInfo, GameRound

class GameRoundSerializer(serializers.ModelSerializer):

	class Meta:
		model = GameRound
		fields = ('pk', 'is_completed', 'player_info', 'game_info', 'article', 'start_time', 'end_time', 'duration',
					'is_completed', 'chunk2_requested', 'chunk3_requested', 'show_info_requested', 'player_guess', 'guess_correct',
					'potential_score', 'actual_score', )

class GameRoundStatusSerializer(serializers.ModelSerializer):

	class Meta:
		model = GameRound
		fields = ('chunk2_requested', 'chunk3_requested', 'show_info_requested')

class GameInfoSerializer(serializers.ModelSerializer):

	game_rounds = GameRoundSerializer(many=True, read_only=True)

	class Meta:
		model = GameInfo
		fields = ('pk', 'player_info', 'total_score', 'max_passes', 'total_passes', 'is_completed', 'difficulty', 'max_rounds', 'feedback_version', 'scoring_version', 
					'created_time', 'modified_time', 'current_round', 'current_round_index', 'game_round_list', 'game_rounds',)

class GameInfoShortSerializer(serializers.ModelSerializer):

	class Meta:
		model = GameInfo
		fields = ('pk', 'player_info', 'total_score', 'is_completed', 'difficulty', 'max_rounds', 'feedback_version', 'scoring_version', 
					'created_time', 'modified_time', 'current_round', 'current_round_index', 'game_round_list')

class PlayerInfoSerializer(serializers.ModelSerializer):
	game_infos = GameInfoShortSerializer(many=True, read_only=True)

	class Meta:
		model = PlayerInfo
		fields = ('pk', 'username', 'has_completed_survey', 'age', 'gender', 'education', 'computer_use', 
					'news_media_savvy', 'news_source', 'current_game', 'game_infos',)
		read_only_fields = ('pk', 'current_game', 'game_infos',)


