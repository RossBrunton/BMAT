# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_settings_no_analytics'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='no_ads',
            field=models.BooleanField(default=False),
        ),
    ]
