import json

from django.contrib.gis.geos import Point, Polygon, GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Sum, Avg
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Field
from .serializers import FieldSerializer


class FieldViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        latitude = float(request.query_params.get('latitude'))
        longitude = float(request.query_params.get('longitude'))
        radius = float(request.query_params.get('radius', 1000))  # radius in meters
        crop = request.query_params.get('crop')

        point = Point(longitude, latitude, srid=4326)
        fields = Field.objects.filter(geometry__distance_lte=(point, radius)).only('geometry', 'id', 'crop')
        if crop:
            fields = fields.filter(crop=crop)

        fields = fields.annotate(distance=Distance('geometry', point)).order_by('distance')
        return Response(FieldSerializer(fields, many=True).data)

    @action(detail=False, methods=['post'])
    def inside(self, request):
        coordinates = request.data.get('coordinates')
        polygon = Polygon(coordinates, srid=4326)
        crop = request.query_params.get('crop')

        fields = Field.objects.filter(geometry__within=polygon).only('geometry', 'id', 'crop')
        if crop:
            fields = fields.filter(crop=crop)

        return Response(FieldSerializer(fields, many=True).data)

    @action(detail=False, methods=['post'])
    def intersect(self, request):
        geometry_data = request.data.get('geometry')

        # Convert dict to GeoJSON string
        if isinstance(geometry_data, dict):
            geometry_data = json.dumps(geometry_data)

        geometry = GEOSGeometry(geometry_data, srid=4326)
        crop = request.query_params.get('crop')

        fields = Field.objects.filter(geometry__intersects=geometry).only('geometry', 'id', 'crop')
        if crop:
            fields = fields.filter(crop=crop)

        return Response(FieldSerializer(fields, many=True).data)

    @action(detail=False, methods=['get'])
    def region_stats(self, request):
        region_code = request.query_params.get('region')

        fields = Field.objects.filter(region=region_code).only('area_ha', 'productivity')

        total_area = fields.aggregate(Sum('area_ha'))['area_ha__sum'] or 0
        total_yield = fields.aggregate(Sum('productivity'))['productivity__sum'] or 0
        weighted_avg_yield = fields.aggregate(Avg('productivity'))['productivity__avg'] or 0

        return Response({
            'total_area_ha': total_area,
            'total_yield': total_yield,
            'weighted_average_yield': weighted_avg_yield
        })