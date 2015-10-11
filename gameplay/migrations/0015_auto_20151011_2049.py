# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0014_auto_20151010_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameinfo',
            name='actual_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='got_bonus',
            field=models.BooleanField(default=False),
        ),
    ]
