from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from rest_framework.response import Response
from rest_framework import generics
from .models import Field
from .serializers import FieldSerializer

class NearbyFieldsView(generics.ListAPIView):
    serializer_class = FieldSerializer

    def get_queryset(self):
        latitude = float(self.request.query_params.get('latitude'))
        longitude = float(self.request.query_params.get('longitude'))
        radius = float(self.request.query_params.get('radius', 1000))

        user_location = Point(longitude, latitude, srid=4326)

        return Field.objects.filter(geometry__distance_lte=(user_location, radius))

class InsideParallelogramView(generics.ListAPIView):
    serializer_class = FieldSerializer

    def get_queryset(self):
        vertices = self.request.query_params.get('vertices').split('|')
        points = [tuple(map(float, v.split(','))) for v in vertices]
        polygon = Polygon(points, srid=4326)
        return Field.objects.filter(geometry__within=polygon)

class IntersectingFieldsView(generics.ListAPIView):
    serializer_class = FieldSerializer

    def get_queryset(self):
        # Geometry passed as GeoJSON
        geometry = self.request.data.get('geometry')
        return Field.objects.filter(geometry__intersects=geometry)
