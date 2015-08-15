# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0002_auto_20150810_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameinfo',
            name='player_info',
            field=models.ForeignKey(related_name='game_infos', to='gameplay.PlayerInfo'),
        ),
        migrations.AlterField(
            model_name='gameround',
            name='player_guess',
            field=models.CharField(default=b'', max_length=16, blank=True),
        ),
    ]
