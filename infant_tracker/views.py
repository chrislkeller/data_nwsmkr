from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext, Context, loader
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, Http404
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q, Avg, Max, Min, Sum, Count
from django import forms
from .models import Event
import os
import calculate
import time
import datetime
from datetime import tzinfo
import pytz
from pytz import timezone
from dateutil import parser
import logging
import yaml
import calendar
import math

logger = logging.getLogger('data_nwsmkr')

class EventIndex(ListView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super(EventIndex, self).get_context_data(**kwargs)
        context['object_list'] = Event.objects.order_by('-created_at')

        # if i want to round to nearest five minute increment
        test_time = context['object_list'][0].created_at
        test_time += datetime.timedelta(minutes=5)
        test_time -= datetime.timedelta(minutes=test_time.minute % 5, seconds=test_time.second, microseconds=test_time.microsecond)

        # try to display elapsed time
        current_time = pytz.utc.localize(datetime.datetime.utcnow())
        current_event = context['object_list'][0].created_at
        previous_event = context['object_list'][1].created_at
        elapsed_time = current_time - current_event
        context['elapsed_time'] = elapsed_time


        context['last_bottle'] = Event.objects.order_by('-created_at').filter(event_type="BTL")

        logger.debug(context['last_bottle'][0].created_at)



        return context


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'event_type',
            'event_notes',
        ]

        widgets = {
            'event_type': forms.RadioSelect,
        }


class EventCreate(CreateView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('infant_tracker:event-index')


class EventUpdate(UpdateView):
    model = Event
    fields = [
        'created_at',
        'event_type',
        'event_notes',
    ]
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('infant_tracker:event-index')


class EventDelete(DeleteView):
    model = Event
    success_url = reverse_lazy('infant_tracker:event-index')
