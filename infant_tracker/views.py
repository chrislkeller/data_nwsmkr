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
import datetime
import logging
import yaml
import calendar
import math

logger = logging.getLogger('data_nwsmkr')

class EventIndex(ListView):
    model = Event
    def get_context_data(self, **kwargs):
        context = super(EventIndex, self).get_context_data(**kwargs)
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
