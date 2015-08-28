# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0009_auto_20150822_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameinfo',
            name='max_time',
            field=models.IntegerField(default=180),
        ),
        migrations.AlterField(
            model_name='playerinfo',
            name='news_source',
            field=models.CharField(default=b'', max_length=36, blank=True),
        ),
    ]
