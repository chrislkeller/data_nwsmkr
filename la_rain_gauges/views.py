from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext, Context, loader
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, Http404, StreamingHttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse, reverse_lazy
from .models import RainGauge, RainGaugeReading
from googlegeocoder import GoogleGeocoder
import calculate
from haversine import haversine
# import os
# import time
# import datetime
# from datetime import tzinfo
# import pytz
# from pytz import timezone
# from dateutil import parser
import logging
# import yaml
# import calendar
# import math

logger = logging.getLogger('data_nwsmkr')

def main_page(request):
    if request.method=='GET':
        token = request.GET['token']
        if token == 'QHo1Fl7oVvh4QTIJLZkbCet7':
            user_name = request.GET.get('user_name', '')
            zip_code = request.GET.get('text', '')
            list_of_nearby_gauges = []
            rain_gauges = RainGauge.objects.filter(gauge_type="automatic")
            geocoder = GoogleGeocoder()
            try:
                search = geocoder.get(zip_code)
                if len(search) > 0:
                    first_result = search[0]
                    lat = first_result.geometry.location.lat
                    lng = first_result.geometry.location.lng
                else:
                    lat = None
                    lng = None
            except Exception, exception:
                logger.error("%s" % (exception))
            if lat != None and lng != None:
                this_location = (lat, lng)
                for gauge in rain_gauges:
                    comparison_gauge = (gauge.lat_converted, gauge.lng_converted)
                    evaluated_distance = haversine(this_location, comparison_gauge)
                    if evaluated_distance < 10:
                        gauge.distance = float("{0:.2f}".format(evaluated_distance))
                        list_of_nearby_gauges.append(gauge)
                message = "Hello %s. Here are the rain gauges within 10 miles of the %s\n" % (user_name, zip_code)
                for item in list_of_nearby_gauges:
                    message += "\t* %s - %s miles\n" % (item.station_name, item.distance)
                    gauge = RainGauge.objects.get(id=item.id)
                    gaugereadings = gauge.raingaugereading_set.order_by("-reading_date_time")
                    gauge_accumulation = gaugereadings[0].reading_accumulated
                    gauge_reading = gaugereadings[0].reading_date_time.strftime("%I:%M %p %Z on %a, %b %d, %Y")
                    message += "\t\t* %s inches as of %s\n" % (gauge_accumulation, gauge_reading)
            else:
                message = "Hello %s. We couldn't retrieve any data for you"
            return StreamingHttpResponse(message)
        else:
            return StreamingHttpResponse('we could not handle your request')
    else:
        return StreamingHttpResponse('we could not handle your request')
