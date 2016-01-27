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

class Event(models.Model):

    WOKE = "WKE"
    NURSED = "NRS"
    NAPPED = "NPD"
    BOTTLE = "BTL"
    ACTIVITY = "ACT"
    BEDTIME = "BED"

    CHOICES = (
        (WOKE, "Woke"),
        (NURSED, "Nursed"),
        (NAPPED, "Napped"),
        (BOTTLE, "Bottle"),
        (ACTIVITY, "Activity"),
        (BEDTIME, "Bedtime"),
    )

    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    event_type = models.CharField("What Happened", max_length=3, choices=CHOICES, default=1)
    event_notes = models.TextField("Event Notes", blank=True, null=True, default=None)

    def __unicode__(self):
        return self.event_type

    def get_absolute_url(self):
        return reverse("event-update", kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
