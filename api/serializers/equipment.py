from country_list import countries_for_language
from rest_framework import serializers
from rest_framework.reverse import reverse

from api.models import Equipment
from modec.settings import LANGUAGE_CODE


class EquipmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Equipment model
    """
    class Meta:
        """
        Equipment Serializer meta
        """
        model = Equipment
        fields = ['id', 'name', 'code', 'location']
        extra_kwargs = {
            'vessel_id': {'read_only': True}
        }

    def validate(self, data):
        """
        Validate additionally if equipment location is a valid country name
        :param data: Equipment data dict
        :return:
        """
        if 'location' in data and data['location'] not in dict(countries_for_language(LANGUAGE_CODE)).values():
            raise serializers.ValidationError(f'Location "{data["location"]}" is invalid. A country is expected')

        return super().validate(data)
