# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0016_remove_article_source_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='notes',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
