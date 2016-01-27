# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('la_rain_gauges', '0002_auto_20160106_0815'),
    ]

    operations = [
        migrations.AddField(
            model_name='raingauge',
            name='calculated_id',
            field=models.CharField(null=True, max_length=255, blank=True, unique=True, verbose_name=b'Gauge ID', db_index=True),
        ),
    ]
