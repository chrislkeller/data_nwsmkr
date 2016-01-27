# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('la_rain_gauges', '0003_raingauge_calculated_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='RainGaugeReading',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reading_date_time', models.DateTimeField(verbose_name=b'Date & Time of reading')),
                ('reading_raw_count', models.IntegerField(null=True, verbose_name=b'Raw count', blank=True)),
                ('reading_amount', models.FloatField(null=True, verbose_name=b'Rainfall Amount', blank=True)),
                ('reading_accumulated', models.FloatField(null=True, verbose_name=b'Rainfall Accumulation', blank=True)),
                ('calculated_id', models.ForeignKey(to='la_rain_gauges.RainGauge', to_field=b'calculated_id')),
            ],
        ),
    ]
