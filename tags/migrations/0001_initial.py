# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(max_length=100)),
                ('colour', models.CharField(default='white', max_length=20, choices=[('white', 'White'), ('black', 'Black'), ('darkblue', 'Dark Blue'), ('darkgreen', 'Dark Green'), ('darkred', 'Dark Red'), ('blue', 'Blue'), ('green', 'Green'), ('red', 'Red'), ('yellow', 'Yellow'), ('magenta', 'Magenta'), ('cyan', 'Cyan'), ('orange', 'Orange')])),
                ('slug', models.SlugField()),
                ('implies', models.ManyToManyField(related_name='implied_by', to='tags.Tag')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['slug'],
            },
            bases=(models.Model,),
        ),
    ]
