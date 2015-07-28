# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20150721_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_type',
            field=models.CharField(max_length=32, choices=[(b'news', b'News'), (b'advertising', b'Advertising'), (b'opinion', b'Opinion'), (b'entertainment', b'Entertainment')]),
        ),
        migrations.AlterField(
            model_name='article',
            name='difficulty',
            field=models.CharField(max_length=16, choices=[(b'easy', b'easy'), (b'medium', b'medium'), (b'hard', b'hard')]),
        ),
    ]
