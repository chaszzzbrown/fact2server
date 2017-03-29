# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_auto_20150808_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='articleType',
            field=models.CharField(default=b'news', max_length=32, choices=[(b'news', b'News'), (b'notNews', b'Not News')]),
        ),
        migrations.AddField(
            model_name='article',
            name='body',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='payoffContent',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='payoffSourceLabel',
            field=models.TextField(default=b'', max_length=160, blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='payoffSourceUrl',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='sourceHint',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='article_type',
            field=models.CharField(default=b'news', max_length=32, choices=[(b'news', b'News'), (b'notNews', b'Not News'), (b'advertising', b'Advertising'), (b'opinion', b'Opinion'), (b'entertainment', b'Entertainment')]),
        ),
    ]
