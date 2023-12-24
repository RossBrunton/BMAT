# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='theme',
            field=models.CharField(default='grey_boxes', max_length=10, choices=[('grey_boxes', 'Grey Boxes')]),
            preserve_default=True,
        ),
    ]
