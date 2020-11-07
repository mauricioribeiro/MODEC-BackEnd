from rest_framework import generics

from api.models import Vessel
from api.serializers.vessel import VesselSerializer


class VesselView:
    """
    Abstract view for vessel HTTP resources
    """
    model = Vessel
    queryset = Vessel.objects.filter(status=True)
    serializer_class = VesselSerializer


class VesselListView(VesselView, generics.ListAPIView, generics.CreateAPIView):
    """
    View for list and create vessels over HTTP rest
    """
    view_name = 'vessel-list'


class VesselDetailView(VesselView, generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    """
    View for retrieve a single vessel, update and destroy vessels over HTTP rest
    """
    lookup_field = 'code'
    view_name = 'vessel-detail'
