#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.conf import settings
import csv
from csvkit.utilities.in2csv import In2CSV
import re
import requests
import logging
import time
import datetime
from datetime import tzinfo
import pytz
from pytz import timezone
from dateutil import parser
import os.path

logger = logging.getLogger("gauging_rainfall")

# Create your tests here.
class TestFetchUsageStats(TestCase):
    """
    """

    test_url = "http://dpw.lacounty.gov/wrd/Precip/alert_rain/season_raindata.cfm?id=486"

    url_failures = []

    date_string = "01-05-2016 08:17 AM"

    list_of_potential_ints = [
        "This Could",
        " This Could ",
        "2,354",
        " 2,354 ",
        2354,
        "235,409",
        " 235,409 ",
        235409,
        3.1415,
        " 3.1415 ",
        -1,
        "42262",
        42262,
        "5060.7",
        5060.7,
        "6528.4",
        6528.4,
        "1001.5",
        1001.5,
        "221.27",
        221.27,
        "472853",
        472853,
        "237081000",
        237081000,
        "237,081,000",
        "61",
        "65.65",
        "75.27",
        "0.0343",
        0.0343,
        {"nonstring": "none"}
    ]


    def _test_can_get_response_success_from_url(self):
        """
        test if able to get response from url
        """
        try:
            logger.info("Requesting %s" % (self.test_url))
            response = requests.get(self.test_url, headers=None, timeout=6)
            self.assertEquals(response.status_code, 200)
            self.assertIsNotNone(response.content)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as exception:
            error_output = "%s %s" % (exception, url)
            logger.error(error_output)
            self.url_failures.append(url)
        logger.info(self.url_failures)


    def test_can_make_string_to_utc_datetime(self):
        """
        """
        utc = pytz.timezone("UTC")
        local_tz = pytz.timezone ("America/Los_Angeles")

        raw_date_time = self.date_string.replace("\xc2\xa0", " ").strip()
        self.assertIs(type(raw_date_time), str)

        naive_date_time = datetime.datetime.strptime(raw_date_time, "%m-%d-%Y %I:%M %p")
        self.assertIs(type(naive_date_time), datetime.datetime)

        local_date_time = local_tz.localize(naive_date_time)
        self.assertIsNotNone(local_date_time.tzinfo)
        self.assertEqual(local_date_time.tzname(), "PST")

        utc_date_time = local_date_time.astimezone(utc)
        self.assertIsNotNone(utc_date_time.tzinfo)
        self.assertEqual(utc_date_time.tzname(), "UTC")

        self.assertTrue(utc_date_time > datetime.datetime(2015, 9, 1, 0, 5, 0, 0, pytz.UTC))


    def test_can_convert_str_to_num(self):
        """
        can this value be converted to an int
        http://stackoverflow.com/a/16464365
        """
        for value in self.list_of_potential_ints:

            status = {}

            # actually integer values
            if isinstance(value, (int, long)):
                status["convert"] = True
                status["value"] = value
                self.assertIs(type(value), int)
                self.assertEqual(status["convert"], True)

            # some floats can be converted without loss
            elif isinstance(value, float):
                status["convert"] = (int(value) == float(value))
                status["value"] = value
                self.assertEqual(status["convert"], False)

            # we can't convert non-string
            elif not isinstance(value, basestring):
                status["convert"] = False
                status["value"] = "Nonstring"
                self.assertEqual(status["convert"], False)

            else:
                value = value.strip()
                try:
                    # try to convert value to float
                    float_value = float(value)
                    status["convert"] = True
                    status["value"] = float_value
                    self.assertIs(type(float_value), float)
                    self.assertEqual(status["convert"], True)
                except ValueError:
                    # if fails try to convert value to int
                    try:
                        int_value = int(value)
                        status["convert"] = True
                        status["value"] = int_value
                        self.assertIs(type(int_value), int)
                        self.assertEqual(status["convert"], True)
                    # if fails it's a string
                    except ValueError:
                        status["convert"] = False
                        status["value"] = "String"
                        self.assertIs(type(value), str)
                        self.assertEqual(status["convert"], False)

            self.assertIsNotNone(status)
            self.assertIs(type(status), dict)
            self.assertEqual(status.has_key("convert"), True)
            self.assertEqual(status.has_key("value"), True)
