# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0010_auto_20150827_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameinfo',
            name='game_bonus',
            field=models.IntegerField(default=0),
        ),
    ]
