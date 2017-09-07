# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tags', '0005_auto_20150902_1234'),
    ]

    operations = [
        migrations.CreateModel(
            name='Autotag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pattern', models.CharField(max_length=200)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(related_name='autotags', to='tags.Tag')),
            ],
            options={
                'ordering': ['-added'],
            },
        ),
    ]
