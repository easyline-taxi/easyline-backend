import requests
from random import randint
import logging
import configs
import json
import asyncio
from websockets import connect

# Cria situação anterior
import test_create_situation

url_base = configs.url_base
urls_tests = []
url_base_websocket = configs.url_base.replace('http', 'ws').replace('/api','')
server = url_base_websocket+'/ws/row/?authorization=Bearer%20{}'

print("Test Point Situation")

users = test_create_situation.users
points = test_create_situation.points
users_pranceteiros = []

point_test = points[1].get("id")

for user in users:
    token = 'Bearer {}'.format(user.get('token'))
    headers={'Authorization': token }
    res = requests.post(url=url_base+'/point/', headers=headers, json={"point":point_test})

token = 'Bearer {}'.format(configs.prancheteiro1.get('token'))
headers={'Authorization': token }
res = requests.get(url=url_base+'/point/', headers=headers)
configs.request_print(res)

token = 'Bearer {}'.format(configs.motorista3.get('token'))
headers={'Authorization': token }
res = requests.post(url=url_base+'/point/register/', headers=headers,json={"name": "Meu ponto Teste", "city": "Brasilia", "country": "DF"})
configs.request_print(res)

token = 'Bearer {}'.format(configs.prancheteiro1.get('token'))
headers={'Authorization': token }
res = requests.get(url=url_base+'/point/row/', headers=headers)
configs.request_print(res)


# WEBSOCKET part

# async def SET_LOCALE(uri):
#     async with connect(uri) as websocket:
#          # dentro do ponto
#         object_send = {
#             "action":"SET_LOCALE",
#             "params": {
#                 "coordinate":{
#                     "latitude": 4.3690611867266,
#                     "longitude": 2.868803015787
#             }
#         }
#         }
#         # fora do ponto
#         object_send1 = {
#             "action":"SET_LOCALE",
#             "params": {
#                 "coordinate":{
#                     "latitude": 400.3690611867266,
#                     "longitude": 200.868803015787
#             }
#         }
#         }
#         response = ''
#         count = 0
#         multiply = 1
#         # Looping de aguardo
#         while True:
           
#             if count*multiply >= 7*multiply:
#                 count = 0
#             if count*multiply >= 3*multiply and count*multiply <=3*multiply:
#                 await websocket.send(json.dumps(object_send))
#             if count*multiply > 3*multiply and count*multiply <=6*multiply:
#                 await websocket.send(json.dumps(object_send1))
#             count +=1
#             try:
#                 response = await asyncio.wait_for(websocket.recv(),timeout=200)
#                 print(response)
#             except asyncio.TimeoutError:
#                 pass
async def SET_LOCALE(uri):
    async with connect(uri) as websocket:
         # dentro do ponto
        object_send = {
            "action":"SET_LOCALE",
            "params": {
                "coordinate":{
                    "latitude": 4.3690611867266,
                    "longitude": 2.868803015787
            }
        }
        }
        response = ''

        # Looping de aguardo
        
        await websocket.send(json.dumps(object_send))
        try:
            response = await asyncio.wait_for(websocket.recv(),timeout=200)
            print(response) 
        except asyncio.TimeoutError:
            pass
           
            
async def main_async():
    await asyncio.gather(SET_LOCALE(server.format(configs.motorista1.get('token'))),SET_LOCALE(server.format(configs.motorista2.get('token'))))

asyncio.run(main_async())

res = requests.get(url=url_base+'/point/row/', headers=headers)
print(res.content)
configs.request_print(res)

us = res.json().get('data')
res = requests.put(url=url_base+'/point/row/', headers=headers, json={"user":us[0].get('user_id'),"position":2}) 
configs.request_print(res)

res = requests.post(url=url_base+'/point/row/', headers=headers, json={"user":us[1].get('user_id')}) 
configs.request_print(res)

res = requests.get(url=url_base+'/point/row/', headers=headers)
print(res.content)
configs.request_print(res)

print("Test Point Situation Completed")