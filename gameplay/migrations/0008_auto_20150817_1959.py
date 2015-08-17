# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0007_auto_20150816_0224'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gameinfo',
            old_name='max_stories',
            new_name='max_rounds',
        ),
    ]
