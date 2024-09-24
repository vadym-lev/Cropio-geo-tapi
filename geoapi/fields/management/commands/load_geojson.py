from django.core.management.base import BaseCommand
from django.contrib.gis.geos import MultiPolygon, Polygon
from fields.models import Field
import json

class Command(BaseCommand):
    help = 'Load GeoJSON data into the Field model'

    def handle(self, *args, **kwargs):
        with open('data/fr-subset.geojsons') as f:
            for line in f:
                data = json.loads(line)

                geometry = data['geometry']
                properties = data['properties']

                if geometry['type'] == 'Polygon':
                    geometry = MultiPolygon(Polygon(*geometry['coordinates']))
                elif geometry['type'] == 'MultiPolygon':
                    polygons = [Polygon(*coords) for coords in geometry['coordinates']]
                    geometry = MultiPolygon(polygons)

                Field.objects.create(
                    crop=properties.get('crop'),
                    productivity=properties.get('productivity'),
                    area_ha=properties['area_ha'],
                    region=properties['region'],
                    score=properties.get('score'),
                    geometry=geometry
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded GeoJSON data'))