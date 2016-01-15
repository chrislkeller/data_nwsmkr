# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RainGauge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('station_id', models.CharField(unique=True, max_length=255, verbose_name=b'Gauge ID', db_index=True)),
                ('station_name', models.TextField(verbose_name=b'Gauge Station Name')),
                ('lat_original', models.CharField(max_length=255, verbose_name=b'Raw latitude')),
                ('lat_degrees', models.IntegerField(null=True, blank=True)),
                ('lat_minutes', models.IntegerField(null=True, blank=True)),
                ('lat_seconds', models.IntegerField(null=True, blank=True)),
                ('lat_converted', models.FloatField(null=True, verbose_name=b'Latitude', blank=True)),
                ('lng_original', models.CharField(max_length=255, verbose_name=b'Raw longitude')),
                ('lng_degrees', models.IntegerField(null=True, blank=True)),
                ('lng_minutes', models.IntegerField(null=True, blank=True)),
                ('lng_seconds', models.IntegerField(null=True, blank=True)),
                ('lng_converted', models.FloatField(null=True, verbose_name=b'Longitude', blank=True)),
                ('gauge_elevation', models.IntegerField(null=True, verbose_name=b'Gauge elevation', blank=True)),
                ('gauge_type', models.CharField(max_length=255, null=True, verbose_name=b'Gauge type', blank=True)),
                ('gauge_description', models.CharField(max_length=255, null=True, verbose_name=b'Gauge description', blank=True)),
                ('gauge_url', models.URLField(max_length=1024, null=True, verbose_name=b'URL to gauge data', blank=True)),
            ],
        ),
    ]
