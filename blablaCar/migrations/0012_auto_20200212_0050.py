# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-02-11 23:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blablaCar', '0011_auto_20200210_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lieuarrivee',
            name='quartier',
            field=models.CharField(blank=True, db_index=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='lieudapart',
            name='quartier',
            field=models.CharField(blank=True, db_index=True, max_length=20, null=True),
        ),
    ]
