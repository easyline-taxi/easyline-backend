
from random import random,randint
import json

def generate_cpf(): 
    """
        Gera um CPF válido
    """                                                       
    cpf = [randint(0, 9) for x in range(9)]                              
                                                                                
    for _ in range(2):                                                          
        val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11      
                                                                                
        cpf.append(11 - val if val > 1 else 0)                                  
                                                                                
    return '%s%s%s%s%s%s%s%s%s%s%s' % tuple(cpf)

def createUser(client):
    """
        Cria um usuário consistente
    """
    number_rand = int(random()*100)
    response = client.post('/api/auth/register/', {
            "email": "teste%d@tester.com" % number_rand,
            "deviceid": number_rand,
            "name": "tester %d" % number_rand,
            "cpf": generate_cpf(),
            "password": "123",
            "confirm_password": "123"
        },content_type="application/json")
    credentials = {
        "email":"teste%d@tester.com" % number_rand,
        "password":"123",
        "deviceid":number_rand
        }
    return response,credentials

def loginUser(client,credentials):
    """
        Faz Login com as credenciais
    """
    response = client.post('/api/auth/login/', {
        "username": credentials.get("email"), 
        "password": credentials.get("password"),
        "deviceid": credentials.get("deviceid")
        },content_type="application/json")
    authorization = 'Bearer ' + response.json().get('token')
    return response,authorization

def createPoint(client,auth):
    """
        Cria um ponto em um determinado usuário
    """
    number_rand = int(random()*100)
    response = client.post(
            '/api/point/register/',
            {
                "name": "point_name_%d" % number_rand,
                "city": "City_name_%d" % number_rand,
                "country": "%d" % int(random()*10)
            },
            HTTP_AUTHORIZATION=auth,content_type="application/json"
        )
    credentials = {
        "name": "point_name_%d" % number_rand,
        "city": "City_name_%d" % number_rand
    }
    return response,credentials

def getDataUser(client,auth):
    response = client.get('/api/user/',HTTP_AUTHORIZATION=auth)
    return response

def selectPointToWork(client,auth,point):
    response = client.post('/api/point/',
    {
        "point": point.get("id")
    },
    HTTP_AUTHORIZATION=auth,content_type="application/json")
    return response

def addUserToPoint(client,auth_owner,user):
    response = client.post("/api/point/actions/",
        {
            "deviceid":user.get("deviceid")
        },HTTP_AUTHORIZATION=auth_owner,content_type="application/json"
    )
    return response

def transferPoint(client,auth_owner,user):
    response = client.put('/api/point/config/', 
            json.dumps({"email":user.get("email")}),
            HTTP_AUTHORIZATION=auth_owner,
            content_type="application/json")
    return response