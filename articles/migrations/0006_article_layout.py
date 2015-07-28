# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_auto_20150721_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='layout',
            field=models.CharField(default='layout1', max_length=16, choices=[(b'layout1', b'Layout 1'), (b'layout2', b'Layout 2'), (b'layout3', b'Layout 3'), (b'layout4', b'Layout 4'), (b'layout5', b'Layout 5')]),
            preserve_default=False,
        ),
    ]
