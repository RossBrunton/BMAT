# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_settings_is_trial'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='hide_settings',
            field=models.BooleanField(default=False),
        ),
    ]
