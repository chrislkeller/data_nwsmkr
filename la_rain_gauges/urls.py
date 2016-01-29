from django.conf import settings
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView
from . import views

app_name = "la_rain_gauges"

urlpatterns = [
    url(r'rainfall-search/?$', views.main_page, name='main_page'),
]
