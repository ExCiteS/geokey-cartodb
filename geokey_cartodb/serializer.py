from json import loads as json_loads

from rest_framework.serializers import BaseSerializer
from rest_framework_gis.serializers import GeoFeatureModelListSerializer


class CartoDbSerializer(BaseSerializer):
    class Meta:
        list_serializer_class = GeoFeatureModelListSerializer

    def to_representation(self, obj):
        location = obj.location

        properties = {}
        for field in obj.category.fields.all():
            value = obj.attributes.get(field.key)
            if value is not None:
                properties[field.key] = field.convert_from_string(value)

        return {
            'id': obj.id,
            'type': 'Feature',
            'geometry': json_loads(obj.location.geometry.geojson),
            'properties': properties,
            'meta': {
                'status': obj.status,
                'creator': obj.creator.display_name,
                'updator': (obj.updator.display_name
                            if obj.updator is not None else None),
                'created_at': obj.created_at,
                'version': obj.version,
                'location': {
                    'id': location.id,
                    'name': location.name,
                    'description': location.description
                }
            }
        }
