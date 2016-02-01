from __future__ import division
from django.conf import settings
from django.core.management.base import BaseCommand
from infant_tracker.models import Event
import csv
import logging
import time
import datetime
from datetime import tzinfo
import pytz
from pytz import timezone
from dateutil import parser

logger = logging.getLogger("root")
logging.basicConfig(
    format = "\033[1;36m%(levelname)s: %(filename)s (def %(funcName)s %(lineno)s): \033[1;37m %(message)s",
    level=logging.DEBUG
)

class TasksForData(object):

    def _init(self, *args, **kwargs):
        self.model_markdown_log("/Users/ckeller/Desktop/infant_tracker_event.csv")

    def model_markdown_log(self, csv_file):
        with open(csv_file, "rb") as csvfile:
            csv_data = csv.DictReader(csvfile, delimiter=',')
            for row in csv_data:
                clean_row = {k.strip(): v.strip() for k, v in row.iteritems()}
                clean_row["created_at"] = self._can_make_string_to_utc_datetime(clean_row["created_at"])
                clean_row["updated_at"] = self._can_make_string_to_utc_datetime(clean_row["updated_at"])
                object = Event(
                    id=clean_row["id"],
                    created_at=clean_row["created_at"],
                    event_type=clean_row["event_type"],
                    updated_at=clean_row["updated_at"],
                    event_notes=clean_row["event_notes"],
                )
                try:
                    logger.debug(object)
                    object.save()
                except:
                    raise

    def _can_make_string_to_utc_datetime(self, date_string):
        """
        """
        utc = pytz.timezone("UTC")
        local_tz = pytz.timezone ("America/Los_Angeles")
        raw_date_time = date_string.strip()
        naive_date_time = parser.parse(raw_date_time)
        local_date_time = local_tz.localize(naive_date_time)
        utc_date_time = local_date_time.astimezone(utc)
        return utc_date_time


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.task_started = datetime.datetime.now()
        task_run = TasksForData()
        task_run._init()
        self.task_finished = datetime.datetime.now()
        self.stdout.write("\nTask start: %s\nTask finish: %s\n" % (str(self.task_started), str(self.task_finished)))
