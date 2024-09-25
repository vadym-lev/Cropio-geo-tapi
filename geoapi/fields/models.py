from django.db import models
from django.contrib.gis.db import models as gis_models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.gis.geos import Polygon, MultiPolygon

class Field(gis_models.Model):
    id = models.AutoField(primary_key=True)
    crop = models.CharField(max_length=100, null=True, blank=True)
    productivity = models.FloatField(null=True, blank=True)
    area_ha = models.FloatField()
    region = models.CharField(max_length=10, null=True)  # ISO 3166-2 code of region
    history = models.JSONField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    geometry = gis_models.MultiPolygonField(srid=4326)

    def __str__(self):
        return f"Field {self.id} - Region {self.region}"

# Signal to automatically convert Polygon to MultiPolygon
@receiver(pre_save, sender=Field)
def convert_polygon_to_multipolygon(sender, instance, **kwargs):
    if isinstance(instance.geometry, Polygon):
        instance.geometry = MultiPolygon(instance.geometry)

