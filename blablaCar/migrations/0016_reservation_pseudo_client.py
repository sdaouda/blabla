# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-04-13 11:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blablaCar', '0015_auto_20200214_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='pseudo_client',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
