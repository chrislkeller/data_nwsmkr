# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-27 06:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infant_tracker', '0002_auto_20160126_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
