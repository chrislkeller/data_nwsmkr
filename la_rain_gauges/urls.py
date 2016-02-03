from django.conf import settings
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView
from .views import NearestRainGauges

app_name = "la_rain_gauges"

urlpatterns = [
    url(r'rainfall-search/?$', NearestRainGauges.as_view(), name='main_page'),
]
