# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-05-26 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blablaCar', '0029_reservation_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientform',
            name='user',
        ),
        migrations.AddField(
            model_name='reservation',
            name='num_vehicule',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.DeleteModel(
            name='ClientForm',
        ),
    ]