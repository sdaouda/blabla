# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-05-21 00:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blablaCar', '0026_clientform_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='phone',
        ),
        migrations.AddField(
            model_name='profile',
            name='telephone',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
