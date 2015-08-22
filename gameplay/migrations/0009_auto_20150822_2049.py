# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0008_auto_20150817_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameround',
            name='actual_score',
            field=models.IntegerField(default=30),
        ),
        migrations.AddField(
            model_name='gameround',
            name='potential_score',
            field=models.IntegerField(default=30),
        ),
    ]
