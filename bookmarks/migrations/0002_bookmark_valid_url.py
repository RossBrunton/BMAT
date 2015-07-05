# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='valid_url',
            field=models.BooleanField(default=False),
        ),
    ]
