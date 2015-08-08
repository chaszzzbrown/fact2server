# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_auto_20150808_0207'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('created_date',)},
        ),
    ]
