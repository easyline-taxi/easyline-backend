from django.test import TestCase, Client


class authTestCase(TestCase):

    def test_login_not_exist_auth_token(self):
        client = Client()
        response = self.client.post(
            '/api/login/', content={"username": "admin@tester.com", "password": "123"})
        self.assertEqual(response.json().get('token'), None)
        self.assertEqual(response.status_code, 400)

    def test_register_auth_token(self):
        client = Client()
        response = self.client.post('/api/register/', {
            "email": "admin@tester.com",
            "deviceid": 22123231,
            "name": "tester",
            "cpf": "12332112332",
            "password": "123",
            "confirm_password": "123"
        })
        self.assertEqual((response.json().get('Nome') != None), True)
        self.assertEqual((response.json().get('Email') != None), True)
        self.assertEqual(response.status_code, 200)
