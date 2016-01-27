from django.conf import settings
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView
from .views import EventIndex, EventCreate, EventUpdate, EventDelete

app_name = "infant_tracker"

urlpatterns = [
    url(r'events/$', EventIndex.as_view(), name='event-index'),
    url(r'^events/add/$', EventCreate.as_view(), name='event-add'),
    url(r'^events/(?P<pk>[0-9]+)/$', EventUpdate.as_view(), name='event-update'),
    url(r'^events/(?P<pk>[0-9]+)/delete/$', EventDelete.as_view(), name='event-delete'),
]
