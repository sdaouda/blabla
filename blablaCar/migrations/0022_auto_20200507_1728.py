# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-05-07 16:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blablaCar', '0021_auto_20200416_2303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reservation',
            options={'permissions': [('can_see_trajet_booked', 'can_delete_trajet_booked')]},
        ),
    ]
