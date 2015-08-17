# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0006_auto_20150816_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameinfo',
            name='was_cancelled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='playerinfo',
            name='has_completed_survey',
            field=models.BooleanField(default=False),
        ),
    ]
