from django.test import TestCase, Client
from api.tests_utils import utils
import json

class TestUserActions(TestCase):
    
    def test_view_data_user(self):
        client = Client()
        
        # ? Cria user e faz login
        response,credentials = utils.createUser(client)
        response,auth = utils.loginUser(client, credentials)

        # ? pegar os dados registrados
        response = utils.getDataUser(client,auth)

        self.assertEqual(response.json().get("user_data") != None,True)

    def test_edit_user(self):
        client = Client()
        
        # ? Cria user e faz login
        response,credentials = utils.createUser(client)
        response,auth = utils.loginUser(client, credentials)

        # ? pegar os dados registrados
        response = utils.getDataUser(client,auth)
        data = response.json()

        response = client.put('/api/user/', 
            json.dumps({"name":"Tester007"}),
            HTTP_AUTHORIZATION=auth,
            content_type="application/json")
        
        self.assertEqual(response.status_code, 200)

        data['user_data']['name'] = "Tester007"
        data2 = utils.getDataUser(client,auth).json()
        
        self.assertEqual(data2 == data, True)


    def test_delete_user(self):
        client = Client()
        
        # ? Cria user e faz login
        response,credentials = utils.createUser(client)
        response,auth = utils.loginUser(client, credentials)

        response = client.delete('/api/user/', HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 200)

        try:
            response,auth = utils.loginUser(client, credentials)
            self.assertEqual(False,True)
        except TypeError:
            self.assertEqual(True,True)
        