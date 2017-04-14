# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay2', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameplay',
            name='game_settings_json',
            field=models.TextField(default=b'{}', blank=True),
        ),
    ]
