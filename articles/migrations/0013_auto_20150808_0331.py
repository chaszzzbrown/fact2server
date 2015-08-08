# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_auto_20150808_0307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='source_URL',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
