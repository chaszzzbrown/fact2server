# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0005_gameinfo_total_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameinfo',
            name='max_passes',
            field=models.IntegerField(default=3),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='total_passes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gameinfo',
            name='total_score',
            field=models.IntegerField(default=0),
        ),
    ]
