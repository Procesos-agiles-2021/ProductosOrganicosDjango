from django.contrib.auth.models import User
from django.test import TestCase, Client
from .models import *
import json
import requests


# Create your tests here.
class MercadosOrganicosTestCase(TestCase):

    #-------------------------------- Pruebas de Catalogo --------------------------------

    def test_list_catalogos_status(self):
        url = '/catalogo/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_count_catalogos_list(self):
        user_model = User.objects.create_user(username='test', password='kd8wke-DE34', first_name='test',
                                              last_name='test', email='test@test.com')
        Catalogo.objects.create(fecha_creacion='2021-03-24', admin_creador=user_model)
        Catalogo.objects.create(fecha_creacion='2021-04-25', admin_creador=user_model)

        response = self.client.get('/catalogo/')
        current_data = json.loads(response.content)
        self.assertEqual(len(current_data), 2)

    def test_verify_first_from_catalogos_list(self):
        user_model = User.objects.create_user(username='test', password='kd8wke-DE34', first_name='test',
                                              last_name='test', email='test@test.com')
        Catalogo.objects.create(fecha_creacion='2021-03-24', admin_creador=user_model)
        Catalogo.objects.create(fecha_creacion='2021-04-25', admin_creador=user_model)

        response = self.client.get('/catalogo/')
        current_data = json.loads(response.content)

        self.assertEqual(current_data[0]['fecha_creacion'], "2021-03-24")
