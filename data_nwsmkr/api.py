from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.serializers import Serializer
from la_rain_gauges.models import RainGauge, RainGaugeReading

class RainGaugeResource(ModelResource):
    class Meta:
        queryset = RainGauge.objects.all()
        resource_name = "rain-gauges"
        fields = [
            "calculated_id",
            "updated_at",
            "created_at",
            "gauge_description",
            "gauge_elevation",
            "gauge_type",
            "gauge_url",
            "id",
            "lat_converted",
            "lng_converted",
            "resource_uri",
            "station_id",
            "station_name",
        ]
        filtering = {
            "calculated_id": ALL,
        }
        allowed_methods = ['get']
        serializer = Serializer(formats=['json'])
        limit = 275
        authentication = ApiKeyAuthentication()


class RainGaugeReadingResource(ModelResource):
    calculated_id = fields.ForeignKey(RainGaugeResource, 'calculated_id')
    class Meta:
        queryset = RainGaugeReading.objects.all()
        resource_name = "rain-gauge-readings"
        fields = [
            "created_at",
            "updated_at",
            "reading_date_time",
            "reading_raw_count",
            "reading_amount",
            "reading_accumulated",
        ]
        allowed_methods = ['get']
        serializer = Serializer(formats=['json'])
        limit = 50
        authentication = ApiKeyAuthentication()
