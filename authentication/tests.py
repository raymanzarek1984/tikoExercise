from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticationTests(APITestCase):
    fixtures = [
        'fixtures/authentication.json'
    ]

    @classmethod
    def setUpTestData(cls):
        super(AuthenticationTests, cls).setUpTestData()
        cls.credentials_admin = {
            'username': 'admin',
            'password': '123456'
        }
        cls.data_new_user = {
            'username': 'newUser',
            'password': '12345678!',
            'password2': '12345678!',
            'email': 'test@tiko.energy',
            'last_name': 'New',
            'first_name': 'User'
        }
        cls.credentials_new_user = {
            'username': cls.data_new_user['username'],
            'password': cls.data_new_user['password']
        }
        cls.url_token_obtain = reverse('authentication:token_obtain_pair')
        cls.url_register = reverse('authentication:register')

    def test_authentication_new_user_ok(self):
        """
        Ensure we can authenticate the new User.
        """
        # Create New User
        response_obtain = self.client.post(self.url_token_obtain, self.credentials_admin, format='json')
        response_create = self.client.post(self.url_register, self.data_new_user, format='json', HTTP_AUTHORIZATION=f"Bearer {response_obtain.data['access']}")

        response_obtain = self.client.post(self.url_token_obtain, self.credentials_new_user, format='json')
        response = self.client.post(self.url_register, self.data_new_user, format='json', HTTP_AUTHORIZATION=f"Bearer {response_obtain.data['access']}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # The User already exists

    def test_register_ok(self):
        """
        Ensure we can register a new User object.
        """
        response_obtain = self.client.post(self.url_token_obtain, self.credentials_admin, format='json')
        response = self.client.post(self.url_register, self.data_new_user, format='json', HTTP_AUTHORIZATION=f"Bearer {response_obtain.data['access']}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().username, 'newUser')

    def test_register_nok(self):
        """
        Ensure we cannot register a new User object.
        """
        response = self.client.post(self.url_register, self.data_new_user, format='json', HTTP_AUTHORIZATION="Bearer invalid")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
