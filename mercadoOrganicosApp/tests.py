from django.test import TestCase
from .models import *
import json


# Create your tests here.
class CatalogoTestCase(TestCase):

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

class CarritoTestCase(TestCase):

    def test_list_carrito_status(self):
        url = '/carrito/1'
        response = self.client.get(url, format='json')
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_agregar_carrito(self):
        self.user = User.objects.create(id=1, username='admin_gal', password='admin_gal', is_active=True, is_staff=True,
                                        is_superuser=True)
        response = self.client.post('/carrito/1', json.dumps(
            {"usuario_id": "1"}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
