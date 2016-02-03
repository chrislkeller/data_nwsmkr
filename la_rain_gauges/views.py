from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext, Context, loader
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, Http404, StreamingHttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils import timezone
from .models import RainGauge, RainGaugeReading
from googlegeocoder import GoogleGeocoder
import calculate
from haversine import haversine
# import os
import time
import datetime
from datetime import tzinfo
import pytz
from pytz import timezone
from dateutil import parser
import logging
# import yaml
# import calendar
# import math

logger = logging.getLogger('data_nwsmkr')

class NearestRainGauges(ListView):

    queryset = RainGauge.objects.filter(gauge_type="automatic")

    list_of_nearby_gauges = []

    def get(self, request):
        if request.method=='GET':
            token = request.GET.get('token', False)
            if token == 'QHo1Fl7oVvh4QTIJLZkbCet7':
            # if token == False:
                user_name = request.GET.get('user_name', '')
                zip_code = request.GET.get('text', None)
                task = FunctionalTasks()
                coordinates = task._get_lat_lng_from(90042)
                if coordinates:
                    this_location = (coordinates["lat"], coordinates["lng"])
                    for gauge in self.queryset:
                        nearby_gauge = task._assemble_list_of_nearby(this_location, gauge)
                        if nearby_gauge:
                            self.list_of_nearby_gauges.append(gauge)
                    message = self._create_response_message(task, user_name, zip_code)
                    return StreamingHttpResponse(message)
                else:
                    return StreamingHttpResponse('The zipcode in your request couldn\'t be processed')
            else:
                return StreamingHttpResponse('Your request failed to include the Slack token')
        else:
            return StreamingHttpResponse('We could not process your request')


    def _create_response_message(self, task, user_name, zip_code):
        if len(self.list_of_nearby_gauges) == 0:
            message = "Hello %s. We couldn't retrieve any data for you about the %s" % (user_name, zip_code)
        else:
            message = "Hello %s. Here are the rain gauges within 10 miles of the %s\n" % (user_name, zip_code)
            for item in self.list_of_nearby_gauges:
                message += "\t* %s - %s miles\n" % (item.station_name, item.distance)
                gauge = RainGauge.objects.get(id=item.id)
                gaugereadings = gauge.raingaugereading_set.order_by("-reading_date_time")
                gauge_accumulation = gaugereadings[0].reading_accumulated
                gauge_reading =task._localize_utc_time(gaugereadings[0].reading_date_time)
                string_gauge_reading = gauge_reading.strftime("%-I:%M %p %Z on %a, %b %-d, %Y")
                message += "\t\t* %s inches accumulated between Oct. 1 and %s\n" % (gauge_accumulation, string_gauge_reading)
                image_link = "https://maps.googleapis.com/maps/api/staticmap?key=AIzaSyCgh93OAbzooidV0OUpIOoc6kTxV5o69do&center=%s,%s&zoom=15&size=640x400&scale=2&maptype=roadmap&markers=%s,%s\n" % (gauge.lat_converted, gauge.lng_converted, gauge.lat_converted, gauge.lng_converted)
                message += image_link
        return message


class FunctionalTasks(object):

    local_tz = pytz.timezone ("America/Los_Angeles")

    def _get_lat_lng_from(self, zip_code):
        """
        """
        zip_code = unicode(zip_code)
        geocoder = GoogleGeocoder()
        try:
            search = geocoder.get(zip_code)
            if len(search) > 0:
                first_result = search[0]
                lat = first_result.geometry.location.lat
                lng = first_result.geometry.location.lng
                return {"lat": lat, "lng": lng}
            else:
                lat = None
                lng = None
                return False
        except Exception, exception:
            logger.error("%s" % (exception))
            return False


    def _assemble_list_of_nearby(self, this_location, gauge):
        """
        """
        comparison_location = (gauge.lat_converted, gauge.lng_converted)
        evaluated_distance = haversine(this_location, comparison_location)
        if evaluated_distance < 10:
            gauge.distance = float("{0:.2f}".format(evaluated_distance))
            return gauge
        else:
            return False


    def _localize_utc_time(self, datetime):
        return datetime.astimezone(self.local_tz)
