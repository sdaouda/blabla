# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-02-04 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blablaCar', '0003_auto_20200204_1521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='trajet',
        ),
        migrations.AddField(
            model_name='reservation',
            name='heure_arrivee',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='heure_depart',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='lieu_arrivee',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='lieu_depart',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='trajet',
            name='date_arrivee',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trajet',
            name='date_depart',
            field=models.DateField(blank=True, null=True),
        ),
    ]
