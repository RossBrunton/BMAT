# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_settings_url_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='no_analytics',
            field=models.BooleanField(default=False),
        ),
    ]
