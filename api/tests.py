from django.test import TestCase, Client
from api.tests_utils import utils

# ! Importar outros tests
from .components.user.tests import *
from .components.point.tests import *

class authTestCase(TestCase):

    def test_login_not_exist_auth_token(self):
        client = Client()
        response,credentials = utils.createUser(client)
        response,auth = utils.loginUser(client, credentials)
        self.assertEqual(response.status_code, 200)

    def test_register_auth_token(self):
        client = Client()
        response,credentials = utils.createUser(client)
        self.assertEqual((response.json().get('Nome') != None), True)
        self.assertEqual((response.json().get('Email') != None), True)
        self.assertEqual(response.status_code, 200)