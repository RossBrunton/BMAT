# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20140921_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='theme',
            field=models.CharField(default='light', max_length=10, choices=[('grey_boxes', 'Grey Boxes'), ('light', 'Light')]),
            preserve_default=True,
        ),
    ]
