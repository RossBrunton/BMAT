# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0002_bookmark_valid_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='title',
            field=models.TextField(max_length=150),
        ),
    ]
