# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-27 06:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infant_tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_notes',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Event Notes'),
        ),
    ]
