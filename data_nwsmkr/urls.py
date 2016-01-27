"""data_nwsmkr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import logging
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib import admin
from tastypie.api import Api
from data_nwsmkr.api import RainGaugeResource, RainGaugeReadingResource

logger = logging.getLogger("gauging_rainfall")

# invoke the api
v1_api = Api(api_name='v1')
v1_api.register(RainGaugeResource())
v1_api.register(RainGaugeReadingResource())

urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),

    # tastypie api
    url(r'^api/', include(v1_api.urls)),

    # batch edit in admin
    url(r"^admin/", include("massadmin.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
