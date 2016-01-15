from __future__ import division
from django.conf import settings
from django.core.management.base import BaseCommand
import time
import datetime
import logging
from la_rain_gauges.fetch_rainfall_stats import GaugePrecipitation

logger = logging.getLogger("gauging_rainfall")

class Command(BaseCommand):
    help = "Begin a request to pull data from la county rain gauges"
    def handle(self, *args, **options):
        self.task_started = datetime.datetime.now()
        task_run = GaugePrecipitation()
        task_run._init()
        self.task_finished = datetime.datetime.now()
        self.stdout.write("\nTask start: %s\nTask finish: %s\n" % (str(self.task_started), str(self.task_finished)))





