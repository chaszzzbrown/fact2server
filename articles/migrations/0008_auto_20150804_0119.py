# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_auto_20150804_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.CharField(default=b'', max_length=160, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='source',
            field=models.CharField(default=b'', max_length=160, blank=True),
        ),
    ]
