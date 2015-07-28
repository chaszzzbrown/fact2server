# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='chunk1',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='chunk2',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='chunk3',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='headline',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
