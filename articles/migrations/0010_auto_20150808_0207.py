# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_auto_20150804_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='source_URL',
            field=models.CharField(default=b'', max_length=160, blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='tone',
            field=models.CharField(default=b'', max_length=80, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='article_type',
            field=models.CharField(default=b'news', max_length=32, choices=[(b'news', b'News'), (b'advertising', b'Advertising'), (b'opinion', b'Opinion'), (b'entertainment', b'Entertainment')]),
        ),
        migrations.AlterField(
            model_name='article',
            name='difficulty',
            field=models.CharField(default=b'easy', max_length=16, choices=[(b'easy', b'easy'), (b'medium', b'medium'), (b'hard', b'hard')]),
        ),
        migrations.AlterField(
            model_name='article',
            name='layout',
            field=models.CharField(default=b'layout1', max_length=16, choices=[(b'layout1', b'Layout 1'), (b'layout2', b'Layout 2'), (b'layout3', b'Layout 3'), (b'layout4', b'Layout 4'), (b'layout5', b'Layout 5')]),
        ),
    ]
