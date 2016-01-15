#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os
import sys
import logging
import urllib2
import string
import re
import csv
import requests
import time
import datetime
from datetime import tzinfo
import pytz
from pytz import timezone
from dateutil import parser
from bs4 import BeautifulSoup
from la_rain_gauges.models import RainGauge, RainGaugeReading

logger = logging.getLogger("gauging_rainfall")

class GaugePrecipitation(object):

    gauge_failures = []

    def _init(self, *args, **kwargs):
        """
        start the whole ball rolling
        """
        gauges = RainGauge.objects.order_by("id").filter(gauge_type="automatic").values("calculated_id", "gauge_type", "gauge_url")
        for gauge in gauges:
            failed_gauge = {}
            gauge_content = self._can_get_response_success_from_url(gauge["gauge_url"])
            if gauge_content == False:
                self.gauge_failures.append(gauge)
            else:
                soup = BeautifulSoup(gauge_content)
                target_data = self._can_parse_data_from(soup, gauge["calculated_id"])
                self._can_build_model_instance_from(target_data)
        logger.info(set(self.gauge_failures))


    def _can_get_response_success_from_url(self, url):
        """
        retrieve response from url and return content
        """
        self.countdown(30)
        try:
            logger.info("Requesting %s" % (url))
            response = requests.get(url, headers=None, timeout=12)
            # response = requests.get(url, headers=settings.REQUEST_HEADERS)
            if response.status_code == 200:
                return response.content
            else:
                return False
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as exception:
            error_output = "%s %s" % (exception, url)
            logger.error(error_output)
            return False


    def _can_parse_data_from(self, soup, calculated_id):
        """
        retrieve response from url and return content
        """
        tables = soup.find_all("table")
        rows = tables[1].find_all("tr")
        list_of_data = []
        for row in rows[1:]:
            data = {}
            cells = row.find_all("td")
            if len(cells) == 4:
                data["calculated_id"] = calculated_id
                data["reading_date_time"] = self._can_make_string_to_utc_datetime(cells[0].text.encode("utf-8"))
                try:
                    data["reading_raw_count"] = int(cells[1].text.strip())
                except ValueError, exception:
                    error_output = "%s %s" % (exception, data)
                    logger.error(error_output)
                    data["reading_raw_count"] = float(cells[1].text.strip())
                try:
                    data["reading_amount"] = float(cells[2].text.strip())
                except ValueError, exception:
                    error_output = "%s %s" % (exception, data)
                    logger.error(error_output)
                    data["reading_amount"] = None
                try:
                    data["reading_accumulated"] = float(cells[3].text.strip())
                except ValueError, exception:
                    error_output = "%s %s" % (exception, data)
                    logger.error(error_output)
                    data["reading_accumulated"] = None
            else:
                data["calculated_id"] = calculated_id
                data["reading_date_time"] = None
                data["reading_raw_count"] = None
                data["reading_amount"] = None
                data["reading_accumulated"] = None
            list_of_data.append(data)
        return list_of_data


    def _can_build_model_instance_from(self, target_data):
        """
        """
        for data in target_data:
            try:
                this_gauge = RainGauge.objects.get(calculated_id = data["calculated_id"])
                reading, created = this_gauge.raingaugereading_set.update_or_create(
                    reading_date_time = data["reading_date_time"],
                    defaults = {
                        "updated_at": self._can_create_utc_datetime(datetime.datetime.now()),
                        "reading_raw_count": data["reading_raw_count"],
                        "reading_amount": data["reading_amount"],
                        "reading_accumulated": data["reading_accumulated"],
                    }
                )
                if created:
                    logger.debug("%s created for %s" % (this_gauge, data["reading_date_time"]))
                else:
                    logger.debug("%s - %s exists" % (this_gauge, data["reading_date_time"]))
                this_gauge.updated_at = self._can_create_utc_datetime(datetime.datetime.now())
                this_gauge.save()
            except ObjectDoesNotExist, exception:
                traceback.print_exc(file=sys.stdout)
                error_output = "%s %s" % (exception, data)
                logger.error(error_output)


    def _can_make_string_to_utc_datetime(self, string):
        """
        """
        utc_tz = pytz.timezone("UTC")
        local_tz = pytz.timezone ("America/Los_Angeles")
        raw_date_time = string.replace("\xc2\xa0", " ").strip()
        naive_date_time = datetime.datetime.strptime(raw_date_time, "%m-%d-%Y %I:%M %p")
        local_date_time = local_tz.localize(naive_date_time)
        utc_date_time = local_date_time.astimezone(utc_tz)
        return utc_date_time


    def _can_create_utc_datetime(self, datetime):
        """
        """
        utc_tz = pytz.timezone("UTC")
        local_tz = pytz.timezone ("America/Los_Angeles")
        naive_date_time = datetime
        local_date_time = local_tz.localize(naive_date_time)
        utc_date_time = local_date_time.astimezone(utc_tz)
        return utc_date_time


    def countdown(self, t):
        for i in xrange(t, 0, -1):
            time.sleep(1)
            sys.stdout.write(str(i)+ " ")
            sys.stdout.flush()
        print "\nrunning tasks\n"


if __name__ == '__main__':
    self.task_started = datetime.datetime.now()
    task_run = GaugePrecipitation()
    task_run._init()
    self.task_finished = datetime.datetime.now()
    logger.debug("\nTask start: %s\nTask finish: %s\n" % (str(self.task_started), str(self.task_finished)))
