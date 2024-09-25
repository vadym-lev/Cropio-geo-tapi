from django.core.management.base import BaseCommand
from django.contrib.gis.geos import MultiPolygon, Polygon
from fields.models import Field
import json


class Command(BaseCommand):
    help = 'Load GeoJSON data into the Field model'

    def handle(self, *args, **kwargs):
        fields_to_create = []

        with open('data/fr-subset.geojsons') as f:
            for line in f:
                data = json.loads(line)

                geometry = self.convert_geometry(data['geometry'])
                properties = data['properties']

                field = Field(
                    id=properties.get('id'),
                    crop=properties.get('crop', None),
                    productivity=properties.get('productivity', None),
                    area_ha=properties['area_ha'],
                    region=properties['region'],
                    history=properties.get('history', None),
                    score=properties.get('score', None),
                    geometry=geometry
                )
                fields_to_create.append(field)

        if fields_to_create:
            Field.objects.bulk_create(fields_to_create)

        self.stdout.write(self.style.SUCCESS('Successfully loaded GeoJSON data'))

    def convert_geometry(self, geometry):
        if geometry['type'] == 'Polygon':
            return MultiPolygon(Polygon(*geometry['coordinates']))
        elif geometry['type'] == 'MultiPolygon':
            polygons = [Polygon(*coords) for coords in geometry['coordinates']]
            return MultiPolygon(polygons)

