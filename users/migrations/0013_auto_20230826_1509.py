# Generated by Django 2.2.28 on 2023-08-26 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20170915_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='theme',
            field=models.CharField(choices=[('grey_boxes', 'Grey Boxes'), ('light', 'Light Glow'), ('dark', 'Dark Dusk')], default='light', max_length=10),
        ),
    ]