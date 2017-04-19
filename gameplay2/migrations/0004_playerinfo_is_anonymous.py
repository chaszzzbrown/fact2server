# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay2', '0003_auto_20170416_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerinfo',
            name='is_anonymous',
            field=models.BooleanField(default=False),
        ),
    ]
