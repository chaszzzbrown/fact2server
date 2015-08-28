# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0011_gameinfo_game_bonus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameinfo',
            name='max_time',
            field=models.IntegerField(default=60),
        ),
    ]
