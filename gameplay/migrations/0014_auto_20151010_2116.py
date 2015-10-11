# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0013_auto_20151010_0249'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameinfo',
            name='low_score_threshold',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='medium_score_threshold',
            field=models.IntegerField(default=200),
        ),
        migrations.AlterField(
            model_name='gamesettings',
            name='game_round_list',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
