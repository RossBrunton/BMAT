# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_auto_20150227_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='pinned',
            field=models.BooleanField(default=False),
        ),
    ]
