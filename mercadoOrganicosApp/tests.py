from django.test import TestCase
from .models import *
import json

from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.


class CatalogoTestCase(TestCase):

    def test_list_catalogos_status(self):
        url = '/catalogo/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_count_catalogos_list(self):
        user_model = User.objects.create_user(username='test', password='kd8wke-DE34', first_name='test',
                                              last_name='test', email='test@test.com')
        Catalogo.objects.create(
            fecha_creacion='2021-03-24', admin_creador=user_model)
        Catalogo.objects.create(
            fecha_creacion='2021-04-25', admin_creador=user_model)

        response = self.client.get('/catalogo/')
        current_data = json.loads(response.content)
        self.assertEqual(len(current_data), 2)

    def test_verify_first_from_catalogos_list(self):
        user_model = User.objects.create_user(username='test', password='kd8wke-DE34', first_name='test',
                                              last_name='test', email='test@test.com')
        Catalogo.objects.create(
            fecha_creacion='2021-03-24', admin_creador=user_model)
        Catalogo.objects.create(
            fecha_creacion='2021-04-25', admin_creador=user_model)

        response = self.client.get('/catalogo/')
        current_data = json.loads(response.content)

        self.assertEqual(current_data[0]['fecha_creacion'], "2021-03-24")


class CarritoTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(id=1, username='admin_gal', password='admin_gal', is_active=True, is_staff=True,
                                        is_superuser=True)

    def test_list_carrito_status(self):
        url = '/carrito/1'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_agregar_carrito(self):
        response = self.client.post('/carrito/1', json.dumps(
            {"usuario_id": "1"}), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_list_item_carrito(self):
        url = '/itemcarrito/1'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_agregar_item_carrito(self):
        Carrito.objects.create(id='1', usuario_id=self.user)
        Catalogo.objects.create(
            id='1', fecha_creacion='2020-11-01', admin_creador=self.user)
        ItemCompra.objects.create(
            id='1', imagenUrl='', visibilidad=True, catalogo_id='1')
        response = self.client.post('/itemcarrito/1', json.dumps(
            {
                "usuario_id": "1",
                "item_compras": [
                    {
                        "itemCompra_id": "1",
                        "cantidad": "1"
                    }
                ]
            }), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_detele_item_carrito(self):
        Carrito.objects.create(id='1', usuario_id=self.user)
        Catalogo.objects.create(
            id='1', fecha_creacion='2020-11-01', admin_creador=self.user)
        ItemCompra.objects.create(
            id='1', imagenUrl='', visibilidad=True, catalogo_id='1')
        ItemCompraCarrito.objects.create(
            carrito_id=1, item_compra_id=1, cantidad=1)
        response = self.client.delete(
            '/itemcarrito/1/itemcompra/1', format='json')
        self.assertEqual(response.status_code, 200)


class RegisterClientTest(APITestCase):
    def test_create_client(self):
        url = '/registerClient/'
        data = {
            "username": "test47",
            "password": "test12345",
            "password2": "test12345",
            "email": "test47@gmail.com",
            "first_name": "Test47",
            "last_name": "test",
            "clientprofile": 1
        }
        response = self.client.post(url, data, format='json')
        return response

    def test_create_producer(self):
        url = '/registerClient/'
        data = {
            "username": "test48",
            "password": "test12345",
            "password2": "test12345",
            "email": "test48@gmail.com",
            "first_name": "Test48",
            "last_name": "test",
            "clientprofile": 2
        }
        response = self.client.post(url, data, format='json')
        return response
