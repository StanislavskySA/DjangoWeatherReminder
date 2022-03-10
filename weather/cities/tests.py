from rest_framework.test import APITestCase, APIClient
from cities.models import User
from django.urls import reverse


# Create your tests here.


class TestView(APITestCase):

    city_url = reverse('city')
    subscribe_url = reverse('subscribed')
    weather_url = reverse('weather')

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        pass

    def test_create_user(self):
        data = {'username': 'test', 'password': 'ABC123'}
        response = self.client.post('/api/weather-auth/login/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_get_subscribed_cities(self):
        user = User.objects.create_user(username='test', password='ABC123')
        self.client.force_authenticate(user)
        response = self.client.get(self.subscribe_url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_subscribed_city(self):
        user = User.objects.create_user(username='test', password='ABC123')
        self.client.force_authenticate(user)
        data = {'user': 1, 'city': 1, 'remind_period': 1}
        response_post = self.client.post(self.subscribe_url, data=data)
        response_get = self.client.get('/api/subscribed_delete_update/1/')
        result = response_get.json()
        self.assertEqual(response_post.status_code, 201)
        self.assertEqual(result['user'], data['user'])
        self.assertEqual(result['city'], data['city'])
        self.assertEqual(result['remind_period'], data['remind_period'])
        self.client.logout()

    def test_get_weather(self):
        user = User.objects.create_user(username='test', password='ABC123')
        self.client.force_authenticate(user)
        data = {'user': 1, 'city': 1, 'remind_period': 1}
        self.client.post(self.subscribe_url, data=data)
        response = self.client.get(self.weather_url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()
