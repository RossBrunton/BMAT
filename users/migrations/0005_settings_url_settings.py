# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20150227_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='url_settings',
            field=models.CharField(choices=[('v', 'Check if URLs are correct'), ('n', 'Allow incorrect URLs'), ('y', 'Allow incorrect URLs, and make them links')], max_length=1, default='v'),
        ),
    ]
