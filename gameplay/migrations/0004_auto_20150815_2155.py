# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0003_auto_20150811_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameround',
            name='guess_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='gameround',
            name='game_info',
            field=models.ForeignKey(related_name='game_rounds', to='gameplay.GameInfo'),
        ),
    ]
