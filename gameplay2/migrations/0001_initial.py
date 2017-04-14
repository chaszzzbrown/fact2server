# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_auto_20170329_2012'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePlay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('was_cancelled', models.BooleanField(default=False)),
                ('total_time_seconds', models.IntegerField(default=0)),
                ('was_correct', models.BooleanField(default=False)),
                ('article', models.ForeignKey(to='articles.Article')),
            ],
        ),
        migrations.CreateModel(
            name='GamePlay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('was_cancelled', models.BooleanField(default=False)),
                ('game_state_json', models.TextField(default=b'{}', blank=True)),
                ('total_score', models.IntegerField(default=0)),
                ('total_time_seconds', models.IntegerField(default=0)),
                ('total_articles_played', models.IntegerField(default=0)),
                ('total_articles_correct', models.IntegerField(default=0)),
                ('maximum_score', models.IntegerField(default=0)),
                ('maximum_articles_played', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='GameSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('game_settings_json', models.TextField(default=b'{}', blank=True)),
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
                ('news_source', models.CharField(default=b'', max_length=36, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('has_completed_survey', models.BooleanField(default=False)),
                ('current_game', models.ForeignKey(blank=True, to='gameplay2.GamePlay', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='gameplay',
            name='player_info',
            field=models.ForeignKey(related_name='game_plays', to='gameplay2.PlayerInfo'),
        ),
        migrations.AddField(
            model_name='articleplay',
            name='player_info',
            field=models.ForeignKey(to='gameplay2.PlayerInfo'),
        ),
    ]
