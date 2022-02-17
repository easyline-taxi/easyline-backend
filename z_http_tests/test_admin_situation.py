import requests
from random import randint
import logging
import pytest
import configs

# Cria situação anterior
import test_create_situation

url_base = configs.url_base
urls_tests = []

print("Test Admin Situation")

users = test_create_situation.users
points = test_create_situation.points
users_admin = []

for user in users:
    token = 'Bearer {}'.format(user.get('token'))
    headers={'Authorization': token }
    res = requests.get(url=url_base+'/admin/config/', headers=headers)
    if res.status_code == 200:
        users_admin.append(user)

# Pega historico
token = 'Bearer {}'.format(configs.admin1.get('token'))
headers={'Authorization': token }
res = requests.post(url=url_base+'/admin/getHistoric/', headers=headers,json={"email": configs.motorista3.get("email")})
configs.request_print(res)

# adiciona usuário no ponto
res = requests.post(url=url_base+'/admin/actions/', headers=headers,json={"email": configs.motorista3.get("email"),"deviceid":configs.motorista3.get("deviceid")})
configs.request_print(res)




# muda função do usuario no ponto
res = requests.put(url=url_base+'/admin/transfer/', headers=headers,json={"email": configs.motorista3.get("email"),"function":"P"})
configs.request_print(res)

# muda função do usuario no ponto
res = requests.put(url=url_base+'/admin/transfer/', headers=headers,json={"email": configs.motorista3.get("email"),"function":"M"})
configs.request_print(res)

# Transfere o ponto para o usuário
res = requests.post(url=url_base+'/admin/transfer/', headers=headers,json={"email": configs.motorista3.get("email")})
configs.request_print(res)


token = 'Bearer {}'.format(configs.motorista3.get('token'))
headers={'Authorization': token }

# usuario entra no ponto
res = requests.post(url=url_base+'/point/', headers=headers, json={"point":points[0].get("id")})
configs.request_print(res)

# Transfere o ponto de volta para o admin
res = requests.post(url=url_base+'/admin/transfer/', headers=headers,json={"email": configs.admin1.get("email")})
configs.request_print(res)


# Seta as coordenadas no ponto
token = 'Bearer {}'.format(configs.admin1.get('token'))
headers={'Authorization': token }
locale = {
    "coordinates": [
            {
            "latitude": 20.96,
            "longitude": 40.57
            },
            {
            "latitude": 60.38,
            "longitude": 70.09
            },
            {
            "latitude": 70.76,
            "longitude": 00.49
            },
            {
            "latitude": 10.72,
            "longitude": 00.23
            },
            {
            "latitude": 20.96,
            "longitude":  40.57
            }
        ]
    }
res = requests.put(url=url_base+'/admin/config/', headers=headers,json=locale)
configs.request_print(res)

# Remove usuario do ponto (Como ele via pegar o device id do cara?)
res = requests.put(url=url_base+'/admin/actions/', headers=headers,json={"motive": "Saiu fora do horário","suject": {"email": configs.motorista3.get("email"), "deviceid":configs.motorista3.get("deviceid")}})
configs.request_print(res)

# deleta o ponto
res = requests.delete(url=url_base+'/admin/config/', headers=headers)
configs.request_print(res)

print("Test Admin Situation Completed")
