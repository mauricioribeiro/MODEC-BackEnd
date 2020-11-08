from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

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
        """
        Implements the creation of an equipment
        It setups the equipment vessel automatically by code given in path parameter
        :param serializer: Equipment serializer
        """
        if 'vessel_code' not in self.kwargs:
            raise serializers.ValidationError({'detail': f'Vessel code is required to save this equipment'})

        vessel = Vessel.objects.filter(code=self.kwargs['vessel_code']).first()

        if vessel is None:
            raise serializers.ValidationError({
                'detail': f'Vessel {self.kwargs["vessel_code"]} not found to save this equipment'
            })

        serializer.save(vessel_id=vessel.id)
        super().perform_create(serializer)


class EquipmentDetailView(EquipmentView, generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    """
    View for retrieve a single equipment, update and destroy equipments over HTTP rest
    """
    lookup_field = 'code'
    view_name = 'equipment-detail'


class EquipmentStatusView(EquipmentView, generics.UpdateAPIView):
    """
    View for manage equipment status (activate and inactivate)
    """
    view_name = 'equipment-status'
    action = None

    def update(self, request, *args, **kwargs):
        """
        Updates a list of equipment status by a given action (obtained from path parameter)
        inherits:
        """
        if self.action not in ['activate', 'inactivate']:
            return Response({'detail': 'Resource not found'}, status=HTTP_404_NOT_FOUND)

        if 'codes' not in request.data or type(request.data['codes']) != list:
            return Response({'detail': 'List of equipment codes is missing in json body. Expected: {"codes": [...]}'})

        updated = Equipment.objects.filter(code__in=request.data['codes']) \
            .update(status=True if self.action is 'activate' else False)

        if not updated:
            return Response({'detail': 'No equipments were found by given codes'}, status=HTTP_204_NO_CONTENT)

        return Response({'detail': 'Equipments status updated successfully'})


class EquipmentActivateView(EquipmentStatusView):
    """
    View for activate a equipment status
    """
    action = 'activate'


class EquipmentInactivateView(EquipmentStatusView):
    """
    View for activate a equipment status
    """
    action = 'inactivate'
