from rest_framework import serializers

from api.models import Vessel


class VesselSerializer(serializers.ModelSerializer):
    """
    Serializer for Vessel model
    """
    class Meta:
        """
        Vessel Serializer meta
        """
        model = Vessel
        fields = ['id', 'code']
