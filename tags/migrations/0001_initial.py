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
                ('colour', models.CharField(default=b'white', max_length=20, choices=[(b'white', b'White'), (b'black', b'Black'), (b'darkblue', b'Dark Blue'), (b'darkgreen', b'Dark Green'), (b'darkred', b'Dark Red'), (b'blue', b'Blue'), (b'green', b'Green'), (b'red', b'Red'), (b'yellow', b'Yellow'), (b'magenta', b'Magenta'), (b'cyan', b'Cyan'), (b'orange', b'Orange')])),
                ('slug', models.SlugField()),
                ('implies', models.ManyToManyField(related_name=b'implied_by', to='tags.Tag')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['slug'],
            },
            bases=(models.Model,),
        ),
    ]
