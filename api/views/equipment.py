from rest_framework import generics
from rest_framework.response import Response

from api.models import Equipment, Vessel
from api.serializers.equipment import EquipmentSerializer


class EquipmentView(generics.GenericAPIView):
    """
    Abstract view for Equipment HTTP resources
    """
    model = Equipment
    queryset = Equipment.objects.filter(status=True)
    serializer_class = EquipmentSerializer


class EquipmentListView(EquipmentView, generics.ListAPIView, generics.CreateAPIView):
    """
    View for list and create equipments over HTTP rest
    """
    view_name = 'equipment-list'

    def perform_create(self, serializer):
        if 'vessel_code' in self.kwargs:
            vessel = Vessel.objects.filter(code=self.kwargs['vessel_code']).first()

            if not vessel:
                return Response({'detail': f'Vessel {self.kwargs["vessel_code"]} not found for save this equipment'})

            serializer.save(vessel_id=vessel.id)
        super().perform_create(serializer)


class EquipmentDetailView(EquipmentView, generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    """
    View for retrieve a single equipment, update and destroy equipments over HTTP rest
    """
    lookup_field = 'code'
    view_name = 'equipment-detail'
