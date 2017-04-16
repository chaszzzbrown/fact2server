# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay2', '0002_gameplay_game_settings_json'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articleplay',
            name='is_completed',
        ),
        migrations.RemoveField(
            model_name='articleplay',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='articleplay',
            name='was_cancelled',
        ),
        migrations.AddField(
            model_name='articleplay',
            name='showed_hint',
            field=models.BooleanField(default=False),
        ),
    ]
