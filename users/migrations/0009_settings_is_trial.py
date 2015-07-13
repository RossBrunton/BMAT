# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20150712_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='is_trial',
            field=models.BooleanField(default=False),
        ),
    ]
