# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20150721_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='article_type',
            field=models.TextField(default=b'news', choices=[(b'news', b'News'), (b'advertising', b'Advertising'), (b'opinion', b'Opinion'), (b'entertainment', b'Entertainment')]),
        ),
        migrations.AddField(
            model_name='article',
            name='difficulty',
            field=models.TextField(default=b'easy', choices=[(b'easy', b'easy'), (b'medium', b'medium'), (b'hard', b'hard')]),
        ),
    ]
