# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0015_auto_20151011_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamesettings',
            name='hint_penalty',
            field=models.IntegerField(default=5),
        ),
    ]
