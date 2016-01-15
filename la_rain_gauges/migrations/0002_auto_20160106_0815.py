# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('la_rain_gauges', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raingauge',
            name='station_id',
            field=models.CharField(max_length=255, verbose_name=b'Gauge ID', db_index=True),
        ),
    ]
