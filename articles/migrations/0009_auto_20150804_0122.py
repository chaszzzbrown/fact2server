# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_auto_20150804_0119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.TextField(default=b'', max_length=160, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='source',
            field=models.TextField(default=b'', max_length=160, blank=True),
        ),
    ]
