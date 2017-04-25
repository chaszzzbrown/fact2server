# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0015_auto_20170425_1845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='source_URL',
        ),
    ]
