import random

from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.test import APITestCase

from api.models import Vessel


class VesselTests(APITestCase):
    """
    Vessel test class for unit tests in Vessel Restful resource
    """

    def __create_vessel(self, code):
        """
        Private method to request vessel creation Restful resource
        :param code: Vessel code
        :return: Response
        """
        url, data = reverse('vessel-list'), {'code': code}
        return self.client.post(url, data, format='json')

    def test_list_vessels(self):
        """
        Tests GET /vessels endpoint by create random vessels and after check json list
        """
        vessels = random.randint(1, 9)
        for i in range(vessels):
            self.__create_vessel(code=f'MV10{i}')

        url = reverse('vessel-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Vessel.objects.count(), vessels)

    def test_create_valid_vessel(self):
        """
        Tests POST /vessels endpoint by passing a valid vessel json
        """
        response = self.__create_vessel(code='MV102')

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Vessel.objects.count(), 1)
        self.assertEqual(Vessel.objects.get().code, 'MV102')

    def test_create_invalid_vessel(self):
        """
        Tests POST /vessels endpoint by passing a invalid vessel json
        with code in wrong pattern (AA000)
        """
        response = self.__create_vessel(code='A$#01')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(Vessel.objects.count(), 0)

    def test_update_vessel(self):
        """
        Tests PUT /vessels endpoint by create and update a vessel
        """
        old_code, new_code = 'MV102', 'MV103'
        self.__create_vessel(code=old_code)

        url, data = reverse('vessel-detail', kwargs={'code': old_code}), {'code': new_code}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Vessel.objects.count(), 1)
        self.assertEqual(Vessel.objects.get().code, new_code)

    def test_delete_vessel(self):
        """
        Tests DELETE /vessels endpoint by create and delete a vessel
        """
        self.__create_vessel(code='MV102')

        url = reverse('vessel-detail', kwargs={'code': 'MV102'})
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Vessel.objects.count(), 0)
