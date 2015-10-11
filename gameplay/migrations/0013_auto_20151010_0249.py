# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0012_auto_20150828_2208'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'easy_std', max_length=16)),
                ('difficulty', models.CharField(max_length=16, choices=[(b'easy', b'easy'), (b'medium', b'medium'), (b'hard', b'hard')])),
                ('max_rounds', models.IntegerField(default=10)),
                ('max_time', models.IntegerField(default=180)),
                ('max_passes', models.IntegerField(default=3)),
                ('correct_article_score', models.IntegerField(default=40)),
                ('incorrect_article_penalty', models.IntegerField(default=10)),
                ('time_bonus', models.IntegerField(default=20)),
                ('low_score_threshold', models.IntegerField(default=10)),
                ('medium_score_threshold', models.IntegerField(default=200)),
                ('game_round_list', models.TextField(default=b'')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='game_category',
            field=models.CharField(default=b'dev', max_length=16),
        ),
        migrations.AlterField(
            model_name='gameinfo',
            name='game_round_list',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='gameinfo',
            name='max_time',
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='game_settings',
            field=models.ForeignKey(default=None, blank=True, to='gameplay.GameSettings', null=True),
        ),
    ]
