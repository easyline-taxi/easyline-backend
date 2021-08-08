from django.test import TestCase, Client
from api.tests_utils import utils
import time


class TestPointUser(TestCase):
    def test_create_user_with_point(self):
        client = Client()

        # ? Cria user e faz login
        response, credentials = utils.createUser(client)
        response, authorization = utils.loginUser(client, credentials)

        # ? logado?
        self.assertEqual((response.json().get("token") != None), True)

        # ? return dados do usuário
        response = client.get("/api/user/", HTTP_AUTHORIZATION=authorization)
        self.assertEqual(response.status_code, 200)

        # ? registrar um ponto
        response, credentials = utils.createPoint(client, authorization)
        self.assertEqual(response.status_code, 200)
        # ? verifica se está anexado ao user
        response = client.get("/api/user/", HTTP_AUTHORIZATION=authorization)

        self.assertEqual(
            credentials.get("name")
            in [x.get("name") for x in response.json().get("point_data")],
            True,
        )

    def test_add_user_in_point(self):
        client = Client()

        # ? Cria user e faz login do user  1
        response, credentials_user1 = utils.createUser(client)
        response, authorization1 = utils.loginUser(client, credentials_user1)

        # ? cria ponto user 1
        response, credentials_point = utils.createPoint(client, authorization1)
        self.assertEqual(response.status_code, 200)

        # ! Setar o ponto de trabalho !!!!
        response = utils.getDataUser(client, authorization1)
        points = response.json().get("point_data")
        response = utils.selectPointToWork(client, authorization1, points[0])
        self.assertEqual(response.status_code, 200)

        # ? Cria user e faz login do user 2
        response, credentials_user2 = utils.createUser(client)
        response, authorization2 = utils.loginUser(client, credentials_user2)

        # ? USer 1 add User 2 ao ponto
        response = utils.addUserToPoint(client, authorization1, credentials_user2)
        self.assertEqual(response.status_code, 200)

        # ? Verify se o usuúario foi adicionado
        response = utils.getDataUser(client, authorization2)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            credentials_point.get("name")
            in [x.get("name") for x in response.json().get("point_data")],
            True,
        )

    def test_transfering_point(self):
        client = Client()
        # ? Cria user e faz login do user  1
        response, credentials_user1 = utils.createUser(client)
        response, authorization1 = utils.loginUser(client, credentials_user1)

        # ? cria ponto user 1
        response, credentials = utils.createPoint(client, authorization1)
        self.assertEqual(response.status_code, 200)

        # ! Setar o ponto de trabalho !!!!
        response = utils.getDataUser(client, authorization1)
        points = response.json().get("point_data")
        response = utils.selectPointToWork(client, authorization1, points[0])
        self.assertEqual(response.status_code, 200)

        # ? Cria user e faz login do user 2
        response, credentials_user2 = utils.createUser(client)
        response, authorization2 = utils.loginUser(client, credentials_user2)

        # ? USer 1 add User 2 ao ponto
        response = utils.addUserToPoint(client, authorization1, credentials_user2)
        self.assertEqual(response.status_code, 200)

        # ?User 1 Transfere o ponto para User 2
        response = utils.transferPoint(client, authorization1, credentials_user2)
        
        self.assertEqual(response.status_code, 200)

        
        response = client.get("/api/user/", HTTP_AUTHORIZATION=authorization2)
        
        self.assertEqual(
            "A" in [x.get("function") for x in response.json().get("point_data")], True
        )
