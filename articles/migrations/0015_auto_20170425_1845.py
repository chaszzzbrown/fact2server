# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_auto_20170329_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='article_type',
        ),
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.RemoveField(
            model_name='article',
            name='chunk1',
        ),
        migrations.RemoveField(
            model_name='article',
            name='chunk2',
        ),
        migrations.RemoveField(
            model_name='article',
            name='chunk3',
        ),
        migrations.RemoveField(
            model_name='article',
            name='difficulty',
        ),
        migrations.RemoveField(
            model_name='article',
            name='layout',
        ),
        migrations.RemoveField(
            model_name='article',
            name='references',
        ),
        migrations.RemoveField(
            model_name='article',
            name='source',
        ),
        migrations.RemoveField(
            model_name='article',
            name='tone',
        ),
    ]
