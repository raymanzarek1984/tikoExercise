from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from events.models import (
    Event
)

User = get_user_model()


class EventTests(APITestCase):
    fixtures = [
        'fixtures/users.json'
    ]

    @classmethod
    def setUpTestData(cls):
        super(EventTests, cls).setUpTestData()
        cls.credentials_foobar = {
            'username': 'foobar',
            'password': '12345678!'
        }
        cls.credentials_johndoe = {
            'username': 'johndoe',
            'password': '12345678!'
        }
        cls.data_create_instance_1 = {
            'name': 'Test event',
            'description': 'This is a test event.',
            'start_date': '2023-03-12',
            'end_date': '2023-03-17'
        }
        cls.data_create_instance_2 = {
            'name': 'Test event',
            'description': 'This is a test event.',
            'start_date': '2023-03-12',
            'end_date': '2023-03-17'
        }
        cls.data_update_instance_1 = {
            'name': 'Test event updated',
            'description': 'This is an updated test event.',
            'start_date': '2023-03-13',
            'end_date': '2023-03-15'
        }
        cls.query_mine = {'mine': True}
        cls.url_token_obtain = reverse('authentication:token_obtain_pair')
        cls.url_event_list = reverse('events:list')
        cls.url_instance_1 = reverse('events:instance', args=[1])

    @property
    def access_token_foobar(self):
        response_obtain = self.client.post(self.url_token_obtain, self.credentials_foobar, format='json')
        return response_obtain.data['access']

    @property
    def access_token_johndoe(self):
        response_obtain = self.client.post(self.url_token_obtain, self.credentials_johndoe, format='json')
        return response_obtain.data['access']
    
    def _create_instance_1(self):
        self.client.post(self.url_event_list, self.data_create_instance_1, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_johndoe}")

    def test_fetch_list(self):
        """
        Ensure we can fetch the list of Event objects.
        """
        response_johndoe = self.client.get(self.url_event_list, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_johndoe}")
        self.assertEqual(response_johndoe.status_code, status.HTTP_200_OK)
        self.assertListEqual(response_johndoe.data, [])

        response_foobar = self.client.get(self.url_event_list, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_foobar}")
        self.assertEqual(response_foobar.status_code, status.HTTP_200_OK)
        self.assertListEqual(response_foobar.data, [])

    def test_create(self):
        """
        Ensure we can create an Event object.
        """
        response = self.client.post(self.url_event_list, self.data_create_instance_1, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_johndoe}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(response.data['name'], 'Test event')

        response_johndoe = self.client.get(self.url_event_list, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_johndoe}")
        self.assertEqual(len(response_johndoe.data), 1)

        response_foobar = self.client.get(self.url_event_list, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_foobar}")
        self.assertEqual(len(response_foobar.data), 1)

    def test_fetch_list_mine(self):
        """
        Ensure we can fetch User's own Event objects only.
        """
        self._create_instance_1()

        response_johndoe = self.client.get(self.url_event_list, self.query_mine, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_johndoe}")
        self.assertEqual(response_johndoe.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_johndoe.data), 1)

        response_foobar = self.client.get(self.url_event_list, self.query_mine, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_foobar}")
        self.assertEqual(response_foobar.status_code, status.HTTP_200_OK)
        self.assertListEqual(response_foobar.data, [])

    def test_get_instance(self):
        """
        Ensure we can fetch User's own Event object only.
        """
        self._create_instance_1()
        
        response_johndoe = self.client.get(self.url_instance_1, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_johndoe}")
        self.assertEqual(response_johndoe.status_code, status.HTTP_200_OK)
        self.assertEqual(response_johndoe.data['name'], 'Test event')

        response_foobar = self.client.get(self.url_instance_1, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_foobar}")
        self.assertEqual(response_foobar.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_instance(self):
        """
        Ensure we can update User's own Event object only.
        """
        self._create_instance_1()

        response_johndoe = self.client.put(self.url_instance_1, self.data_update_instance_1, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_johndoe}")
        self.assertEqual(response_johndoe.status_code, status.HTTP_200_OK)
        self.assertEqual(response_johndoe.data['name'], 'Test event updated')

        response_foobar = self.client.put(self.url_instance_1, self.data_update_instance_1, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_foobar}")
        self.assertEqual(response_foobar.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_instance(self):
        """
        Ensure we can delete User's own Event object only.
        """
        self._create_instance_1()

        response_foobar = self.client.delete(self.url_instance_1, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_foobar}")
        self.assertEqual(response_foobar.status_code, status.HTTP_404_NOT_FOUND)

        response_johndoe = self.client.delete(self.url_instance_1, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_johndoe}")
        self.assertEqual(response_johndoe.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)
