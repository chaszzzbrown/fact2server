# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0004_auto_20150815_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameinfo',
            name='total_score',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
