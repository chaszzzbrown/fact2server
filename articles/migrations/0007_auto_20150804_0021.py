# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_article_layout'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.CharField(default=b'', max_length=80, blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='created_date',
            field=models.DateField(default=datetime.datetime(2015, 8, 4, 0, 21, 16, 279006, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='article',
            name='modified_date',
            field=models.DateField(default=datetime.datetime(2015, 8, 4, 0, 21, 25, 839549, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='references',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='source',
            field=models.CharField(default=b'', max_length=80, blank=True),
        ),
    ]
