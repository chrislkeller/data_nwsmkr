from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404
import logging
import time
import datetime

# model for individual water supplier
class RainGauge(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    calculated_id = models.CharField("Gauge ID", db_index=True, unique=True, max_length=255, null=True, blank=True)
    station_id = models.CharField("Gauge ID", db_index=True, max_length=255)
    station_name = models.TextField("Gauge Station Name")
    lat_original = models.CharField("Raw latitude", max_length=255)
    lat_degrees = models.IntegerField(null=True, blank=True)
    lat_minutes = models.IntegerField(null=True, blank=True)
    lat_seconds = models.IntegerField(null=True, blank=True)
    lat_converted = models.FloatField("Latitude", null=True, blank=True)
    lng_original = models.CharField("Raw longitude", max_length=255)
    lng_degrees = models.IntegerField(null=True, blank=True)
    lng_minutes = models.IntegerField(null=True, blank=True)
    lng_seconds = models.IntegerField(null=True, blank=True)
    lng_converted = models.FloatField("Longitude", null=True, blank=True)
    gauge_elevation = models.IntegerField("Gauge elevation", null=True, blank=True)
    gauge_type = models.CharField("Gauge type", max_length=255, null=True, blank=True)
    gauge_description = models.CharField("Gauge description", max_length=255, null=True, blank=True)
    gauge_url = models.URLField("URL to gauge data", max_length=1024, null=True, blank=True)

    def __unicode__(self):
        return self.station_name

    def save(self, *args, **kwargs):
        super(RainGauge, self).save(*args, **kwargs)


class RainGaugeReading(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    calculated_id = models.ForeignKey(RainGauge, to_field="calculated_id")
    reading_date_time = models.DateTimeField("Date & Time of reading")
    reading_raw_count = models.IntegerField("Raw count", null=True, blank=True)
    reading_amount = models.FloatField("Rainfall Amount", null=True, blank=True)
    reading_accumulated = models.FloatField("Rainfall Accumulation", null=True, blank=True)

    def __unicode__(self):
        return self.reading_date_time.strftime("%Y-%m-%d %H:%M")

    def save(self, *args, **kwargs):
        super(RainGaugeReading, self).save(*args, **kwargs)
