from .models import Field
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class FieldSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Field
        geo_field = "geometry"
        fields = ['id', 'crop', 'productivity', 'region', 'area_ha']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['properties']['productivity_estimation'] = representation['properties'].pop('productivity')
        representation['properties']['region_code'] = representation['properties'].pop('region')

        return representation