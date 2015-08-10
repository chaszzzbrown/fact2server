# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameinfo',
            name='current_round_index',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='gameinfo',
            name='current_round',
            field=models.ForeignKey(blank=True, to='gameplay.GameRound', null=True),
        ),
        migrations.AlterField(
            model_name='playerinfo',
            name='current_game',
            field=models.ForeignKey(blank=True, to='gameplay.GameInfo', null=True),
        ),
    ]
