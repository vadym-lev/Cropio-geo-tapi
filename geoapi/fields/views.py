from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.gis.geos import Point, Polygon, GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Sum, Avg
from .models import Field
from .serializers import FieldSerializer
import json
from django.core.exceptions import ValidationError

class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all().order_by('id')
    serializer_class = FieldSerializer

    # Fields near a point within a given radius
    @action(detail=False, methods=['get'], url_path='nearby')
    def nearby(self, request):
        try:
            latitude = float(request.query_params.get('latitude'))
            longitude = float(request.query_params.get('longitude'))
            radius = float(request.query_params.get('radius', 1000))  # default 1000m
            crop = request.query_params.get('crop')

            point = Point(longitude, latitude, srid=4326)
            fields = Field.objects.filter(geometry__distance_lte=(point, radius))

            if crop:
                fields = fields.filter(crop=crop)

            fields = fields.annotate(distance=Distance('geometry', point)).order_by('distance')[:10000]
            return Response(FieldSerializer(fields, many=True).data)

        except (TypeError, ValueError):
            return Response({'error': 'Invalid or missing parameters'}, status=400)

    # Fields inside a parallelogram
    @action(detail=False, methods=['post'], url_path='inside')
    def inside(self, request):
        try:
            coordinates = request.data.get('coordinates')
            if not coordinates or not isinstance(coordinates, list):
                return Response({'error': 'Invalid or missing coordinates'}, status=400)

            polygon = Polygon(coordinates, srid=4326)
            crop = request.query_params.get('crop')

            fields = Field.objects.filter(geometry__within=polygon)
            if crop:
                fields = fields.filter(crop=crop)

            return Response(FieldSerializer(fields[:10000], many=True).data)

        except Exception as e:
            return Response({'error': str(e)}, status=400)

    # Fields that intersect with a geometry
    @action(detail=False, methods=['post'], url_path='intersect')
    def intersect(self, request):
        try:
            geometry_data = request.data.get('geometry')

            # Convert dict to GeoJSON string
            if isinstance(geometry_data, dict):
                geometry_data = json.dumps(geometry_data)

            geometry = GEOSGeometry(geometry_data, srid=4326)
            crop = request.query_params.get('crop')

            fields = Field.objects.filter(geometry__intersects=geometry)
            if crop:
                fields = fields.filter(crop=crop)

            return Response(FieldSerializer(fields[:10000], many=True).data)
        except (TypeError, ValueError, ValidationError) as e:
            return Response({'error': 'Invalid input: ' + str(e)}, status=400)

    # Yield and area statistics in a region
    @action(detail=False, methods=['get'], url_path='region-stats')
    def region_stats(self, request):
        try:
            region_code = request.query_params.get('region')
            if not region_code:
                return Response({'error': 'Missing region parameter'}, status=400)

            fields = Field.objects.filter(region=region_code)
            total_area = fields.aggregate(Sum('area_ha'))['area_ha__sum'] or 0
            total_yield = fields.aggregate(Sum('productivity'))['productivity__sum'] or 0
            weighted_avg_yield = fields.aggregate(Avg('productivity'))['productivity__avg'] or 0

            return Response({
                'total_area_ha': total_area,
                'total_yield': total_yield,
                'weighted_average_yield': weighted_avg_yield
            })

        except Exception as e:
            return Response({'error': str(e)}, status=400)