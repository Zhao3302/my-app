from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Device

class DeviceTests(APITestCase):
    def test_create_device(self):
        """Тест на створення пристрою (Позитивний кейс)"""
        url = '/api/devices/'  # Твій шлях з 5-ї лаби
        data = {'name': 'Тестовий датчик', 'type': 'IoT', 'status': 'active'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Device.objects.count(), 1)

    def test_get_nonexistent_device(self):
        """Тест на помилку 404 (Негативний кейс)"""
        url = '/api/devices/9999/' 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)