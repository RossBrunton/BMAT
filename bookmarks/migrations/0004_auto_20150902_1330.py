# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0003_auto_20150718_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='title',
            field=models.CharField(db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='url',
            field=models.CharField(db_index=True, max_length=500),
        ),
    ]
