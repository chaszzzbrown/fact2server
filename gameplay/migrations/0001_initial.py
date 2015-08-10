# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_auto_20150808_0331'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('difficulty', models.CharField(max_length=16, choices=[(b'easy', b'easy'), (b'medium', b'medium'), (b'hard', b'hard')])),
                ('max_stories', models.IntegerField(default=10)),
                ('feedback_version', models.CharField(default=b'friendly', max_length=16, choices=[(b'friendly', b'friendly'), (b'snarky', b'snarky')])),
                ('scoring_version', models.IntegerField(default=1)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('game_round_list', models.TextField(default=b'[]')),
            ],
        ),
        migrations.CreateModel(
            name='GameRound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(auto_now=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('chunk2_requested', models.BooleanField(default=False)),
                ('chunk3_requested', models.BooleanField(default=False)),
                ('show_info_requested', models.BooleanField(default=False)),
                ('player_guess', models.CharField(default=b'', max_length=16)),
                ('article', models.ForeignKey(to='articles.Article')),
                ('game_info', models.ForeignKey(to='gameplay.GameInfo')),
            ],
        ),
        migrations.CreateModel(
            name='GameRoundList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_round_list', models.TextField(default=b'[]')),
                ('game_number', models.IntegerField(default=1)),
                ('game_type', models.CharField(default=b'easy', max_length=16, choices=[(b'easy', b'easy'), (b'medium', b'medium'), (b'hard', b'hard')])),
            ],
        ),
        migrations.CreateModel(
            name='PlayerInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=64)),
                ('age', models.IntegerField(default=10)),
                ('gender', models.CharField(default=b'M', max_length=8, choices=[(b'M', b'male'), (b'F', b'female'), (b'T', b'trans'), (b'O', b'other')])),
                ('education', models.CharField(default=b'other', max_length=32, choices=[(b'HS diploma', b'HS diploma'), (b'some college', b'some college'), (b'BS/BA', b'BS/BA'), (b'MS/MA', b'MS/MA'), (b'PhD', b'PhD'), (b'other', b'other')])),
                ('computer_use', models.IntegerField(default=0)),
                ('news_media_savvy', models.IntegerField(default=3, choices=[(1, b'1 - not savvy'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5 - very savvy')])),
                ('news_source', models.CharField(max_length=36)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('current_game', models.ForeignKey(to='gameplay.GameInfo', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='gameround',
            name='player_info',
            field=models.ForeignKey(to='gameplay.PlayerInfo'),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='current_round',
            field=models.ForeignKey(to='gameplay.GameRound', null=True),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='player_info',
            field=models.ForeignKey(to='gameplay.PlayerInfo'),
        ),
    ]
