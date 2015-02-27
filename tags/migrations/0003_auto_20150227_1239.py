# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_auto_20140921_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='colour',
            field=models.CharField(default='white', max_length=20, choices=[('white', 'White'), ('black', 'Black'), ('darkblue', 'Dark Blue'), ('darkgreen', 'Dark Green'), ('darkred', 'Dark Red'), ('blue', 'Blue'), ('green', 'Green'), ('red', 'Red'), ('yellow', 'Yellow'), ('magenta', 'Magenta'), ('cyan', 'Cyan'), ('orange', 'Orange')]),
            preserve_default=True,
        ),
    ]
