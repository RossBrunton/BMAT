# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='implies',
            field=models.ManyToManyField(related_name='tags_to', db_table='tags_tag_implies', to='tags.Tag')
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='implies',
            new_name='tags'
        ),
    ]
