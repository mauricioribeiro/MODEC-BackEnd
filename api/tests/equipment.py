import random

from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.test import APITestCase

from api.models import Equipment


class EquipmentTests(APITestCase):
    """
    Equipment test class for unit tests in Equipment Restful resource
    """

    def __create_equipment(self, vessel_code, code, name, location):
        """
        Private method to request equipment creation Restful resource
        :param vessel_code: Vessel code
        :param code: Equipment code
        :param name: Equipment name
        :param location: Equipment location
        :return: Response
        """
        self.client.post(reverse('vessel-list'), {'code': vessel_code}, format='json')

        url = reverse('equipment-list', kwargs={'vessel_code': vessel_code})
        data = {'code': code, 'name': name, 'location': location}

        return self.client.post(url, data, format='json')

    def test_list_equipments(self):
        """
        Tests GET /vessels/equipments endpoint by create random equipments and after check json list
        """
        equipments = random.randint(1, 9)
        for i in range(equipments):
            self.__create_equipment(vessel_code='MV102', code=f'5310B9D{i}', name='compressor', location='Brazil')

        url = reverse('equipment-list', kwargs={'vessel_code': 'MV102'})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Equipment.objects.count(), equipments)

    def test_create_valid_equipment(self):
        """
        Tests POST /equipments/equipments endpoint by passing a valid equipment json
        """
        response = self.__create_equipment(vessel_code='MV102', code='5310B9D7', name='compressor', location='Brazil')

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Equipment.objects.count(), 1)
        self.assertEqual(Equipment.objects.get().code, '5310B9D7')

    def test_create_invalid_code_equipment(self):
        """
        Tests POST /vessels/equipments endpoint by passing a invalid equipment json
        with code in wrong pattern (alphanumeric)
        """
        response = self.__create_equipment(vessel_code='MV102', code='53&$B9*#', name='compressor', location='Brazil')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(Equipment.objects.count(), 0)

    def test_create_invalid_location_equipment(self):
        """
        Tests POST /vessels/equipments endpoint by passing a invalid equipment json
        with code in wrong location
        """
        response = self.__create_equipment(vessel_code='MV102', code='5310B9D7', name='compressor', location='xxxxx')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(Equipment.objects.count(), 0)

    def test_update_equipment(self):
        """
        Tests PUT /vessels/equipments endpoint by create and update an equipment
        """
        old_code, new_code = '5310B9D7', '5310B9D8'
        response = self.__create_equipment(vessel_code='MV102', code=old_code, name='compressor', location='Brazil')
        data = response.data.copy()

        url = reverse('equipment-detail', kwargs={'vessel_code': 'MV102', 'code': old_code})
        data.update({'code': new_code})
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Equipment.objects.count(), 1)
        self.assertEqual(Equipment.objects.get().code, new_code)
        
    def test_inactivate_equipments(self):
        """
        Tests PUT /equipments/inactivate endpoint by create and inactivate an equipment
        """
        self.__create_equipment(vessel_code='MV102', code='5310B9D7', name='compressor', location='Brazil')

        url, data = reverse('equipment-inactivate'), {'codes': ['5310B9D7']}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Equipment.objects.filter(status=False).count(), 1)
        self.assertEqual(Equipment.objects.filter(status=True).count(), 0)

    def test_delete_equipment(self):
        """
        Tests DELETE /vessels/equipments endpoint by create and delete an equipment
        """
        self.__create_equipment(vessel_code='MV102', code='5310B9D7', name='compressor', location='Brazil')

        url = reverse('equipment-detail', kwargs={'vessel_code': 'MV102', 'code': '5310B9D7'})
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Equipment.objects.count(), 0)
