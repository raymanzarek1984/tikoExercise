from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from events.models import (
    Event,
    EventAttendee
)

User = get_user_model()


class AuthenticationTestMixin:
    """ Should only be used in classes that inherit from APITestCase """

    @classmethod
    def setUpTestData(cls):
        super(AuthenticationTestMixin, cls).setUpTestData()
        cls.credentials_foobar = {
            'username': 'foobar',
            'password': '12345678!'
        }
        cls.credentials_johndoe = {
            'username': 'johndoe',
            'password': '12345678!'
        }
        cls.url_token_obtain = reverse('authentication:token_obtain_pair')

    @property
    def access_token_foobar(self):
        response_obtain = self.client.post(self.url_token_obtain, self.credentials_foobar, format='json')
        return response_obtain.data['access']

    @property
    def access_token_johndoe(self):
        response_obtain = self.client.post(self.url_token_obtain, self.credentials_johndoe, format='json')
        return response_obtain.data['access']


class EventTests(AuthenticationTestMixin, APITestCase):
    fixtures = [
        'fixtures/users.json'
    ]

    @classmethod
    def setUpTestData(cls):
        super(EventTests, cls).setUpTestData()
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
        cls.url_event_list = reverse('events:list')
        cls.url_instance_get_1 = reverse('events:get', args=[1])
        cls.url_instance_update_1 = reverse('events:update', args=[1])
        cls.url_instance_delete_1 = reverse('events:delete', args=[1])

    def _create_instance_1(self):
        # self.client.post(self.url_event_list, self.data_create_instance_1, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_johndoe}")
        Event.objects.create(created_by_id=3, **self.data_create_instance_1)

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

    def test_create_ok(self):
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

    def test_get_ok(self):
        """
        Ensure we can fetch User's own Event object only.
        """
        self._create_instance_1()

        response_johndoe = self.client.get(self.url_instance_get_1, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_johndoe}")
        self.assertEqual(response_johndoe.status_code, status.HTTP_200_OK)
        self.assertEqual(response_johndoe.data['name'], 'Test event')

        response_foobar = self.client.get(self.url_instance_get_1, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_foobar}")
        self.assertEqual(response_foobar.status_code, status.HTTP_200_OK)
        self.assertEqual(response_foobar.data['name'], 'Test event')

    def test_update_ok(self):
        """
        Ensure we can update User's own Event object only.
        """
        self._create_instance_1()

        response_johndoe = self.client.put(self.url_instance_update_1, self.data_update_instance_1, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_johndoe}")
        self.assertEqual(response_johndoe.status_code, status.HTTP_200_OK)
        self.assertEqual(response_johndoe.data['name'], 'Test event updated')

    def test_delete_ok(self):
        """
        Ensure we can delete User's own Event object only.
        """
        self._create_instance_1()

        response_johndoe = self.client.delete(self.url_instance_delete_1, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_johndoe}")
        self.assertEqual(response_johndoe.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)

    def test_update_nok(self):
        """
        Ensure we cannot update other User's Event object.
        """
        self._create_instance_1()

        response_foobar = self.client.put(self.url_instance_update_1, self.data_update_instance_1, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_foobar}")
        self.assertEqual(response_foobar.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_foobar.data['created_by'], 'It is not allowed to edit or delete other users\' events.')

    def test_delete_nok(self):
        """
        Ensure we cannot delete other User's Event object.
        """
        self._create_instance_1()

        response_foobar = self.client.delete(self.url_instance_delete_1, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_foobar}")
        self.assertEqual(response_foobar.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_foobar.data['created_by'], 'It is not allowed to edit or delete other users\' events.')


class EventAttendeeTests(AuthenticationTestMixin, APITestCase):
    fixtures = [
        'fixtures/events.json'
    ]

    @classmethod
    def setUpTestData(cls):
        super(EventAttendeeTests, cls).setUpTestData()
        cls.data_1 = {'event': 1}
        cls.data_2 = {'event': 2}
        cls.data_3 = {'event': 3}
        cls.url_register = reverse('events:register-attendee')
        cls.url_event_list = reverse('events:list')

    def test_register(self):
        """
        Ensure we can register an EventAttendee object.
        """
        response_johndoe = self.client.post(self.url_register, self.data_2, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_johndoe}")
        self.assertEqual(response_johndoe.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EventAttendee.objects.count(), 1)
        self.assertEqual(response_johndoe.data['event'], 2)
        self.assertEqual(response_johndoe.data['user'], 3)

        response_foobar = self.client.post(self.url_register, self.data_3, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_foobar}")
        self.assertEqual(response_foobar.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EventAttendee.objects.count(), 2)
        self.assertEqual(response_foobar.data['event'], 3)
        self.assertEqual(response_foobar.data['user'], 2)

        response_list = self.client.get(self.url_event_list, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_johndoe}")
        self.assertEqual(len(response_list.data[0]['attendees']), 1)
        self.assertEqual(len(response_list.data[1]['attendees']), 1)
        self.assertEqual(len(response_list.data[2]['attendees']), 0)

    def test_unregister(self):
        """
        Ensure we can unregister an EventAttendee object.
        """
        # Register John Doe in the Event ID 2.
        obj = EventAttendee.objects.create(event_id=2, user_id=3)
        url_unregister = reverse('events:unregister-attendee', args=[obj.id])

        # Test unregister from an Event to which the user Foo Bar was not registered
        response_foobar = self.client.delete(url_unregister, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_foobar}")
        self.assertEqual(response_foobar.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_foobar.data['user'], 'It is not allowed to register or unregister other users.')

        # Test unregister from an Event to which the user John Doe was registered
        response_johndoe = self.client.delete(url_unregister, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_johndoe}")
        self.assertEqual(response_johndoe.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(EventAttendee.objects.count(), 0)

    def test_register_nok(self):
        """
        Ensure we cannot register an User to a past Event object.
        """
        response = self.client.post(self.url_register, self.data_1, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_johndoe}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['event'], 'It is not allowed to register or unregister to past events.')

    def test_unregister_nok(self):
        """
        Ensure we cannot unregister an User from a past Event object.
        """
        # Register an EventAttendee in a past Event.
        obj = EventAttendee.objects.create(event_id=1, user_id=2)
        url_unregister = reverse('events:unregister-attendee', args=[obj.id])

        response = self.client.delete(url_unregister, format='json', HTTP_AUTHORIZATION=f"Bearer {self.access_token_johndoe}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['event'], 'It is not allowed to register or unregister to past events.')
