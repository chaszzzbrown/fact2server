from django.forms import widgets

from rest_framework import serializers
from . models import *

'''
class GameSettingsSerializer(serializers.ModelSerializer):

	class Meta:
		model = GameSettings
		fields = ('pk', 'name', 'difficulty', 'max_rounds', 'max_time', 'max_passes', 'correct_article_score', 
						'incorrect_article_penalty', 'time_bonus', 'low_score_threshold', 'medium_score_threshold', 'game_round_list', 'hint_penalty',)

		read_only_fields = ('pk', )

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
					'created_time', 'modified_time', 'current_round', 'current_round_index', 'game_round_list', 'game_rounds', 'total_time', 'max_time', 
					'game_bonus', 'game_category', 'settings_name', 'low_score_threshold', 'medium_score_threshold', 'actual_time', 'got_bonus', 'hint_penalty',)

'''

class GamePlaySerializer(serializers.ModelSerializer):

	class Meta:
		model = GamePlay
		fields = ('created_date', 'modified_date', 'player_info', 'is_completed', 'was_cancelled', 'game_settings', 'game_state',
			'total_score', 'total_time_seconds', 'total_articles_played', 'total_articles_correct', 
			'maximum_score', 'maximum_articles_played', 'pk',)
		read_only_fields = ('pk', 'created_date', 'modified_date',)

class GamePlayShortSerializer(serializers.ModelSerializer):

	class Meta:
		model = GamePlay
		fields = ('created_date', 'modified_date', 'player_info', 'is_completed', 'was_cancelled', 
			'total_score', 'total_time_seconds', 'total_articles_played', 'total_articles_correct', 
			'maximum_score', 'maximum_articles_played', 'pk')
		read_only_fields = ('pk',)

class PlayerInfoSerializer(serializers.ModelSerializer):
	game_plays = GamePlayShortSerializer(many=True, read_only=True)
	current_game = GamePlaySerializer(read_only=True)

	class Meta:
		model = PlayerInfo
		fields = ('pk', 'username', 'has_completed_survey', 'age', 'gender', 'education', 'computer_use', 
					'news_media_savvy', 'news_source', 'current_game', 'game_plays',)
		read_only_fields = ('pk', 'current_game', 'game_plays',)


