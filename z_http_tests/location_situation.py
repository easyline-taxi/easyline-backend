import asyncio
from websockets import connect
import json
import requests
import configs
url_base = configs.url_base.replace('http', 'ws').replace('/api','')

async def GET_ROW(uri):
    async with connect(uri) as websocket:
        
        object_send = {
            "action":"GET_ROW",
            "params": {}
        }
        await websocket.send(json.dumps(object_send))
        response = await websocket.recv()
        print(response)

async def SET_LOCALE(uri):
    async with connect(uri) as websocket:
        
        object_send = {
            "action":"SET_LOCALE",
            "params": {
                "coordinate":{
                    "latitude": 4.3690611867266,
                    "longitude": 2.868803015787
            }
        }
        }
        await websocket.send(json.dumps(object_send))
        response = ''
        # Looping de aguardo
        while True:
            try:
                response = await asyncio.wait_for(websocket.recv(),timeout=200)
                print(response)
            except asyncio.TimeoutError:
                pass
server = url_base+'/ws/row/?authorization=Bearer%20'

res = requests.post(url=configs.url_base+'/auth/login/',json=configs.motorista1)
token1 = res.json().get('token')
res = requests.post(url=configs.url_base+'/auth/login/',json=configs.motorista2)
token2 = res.json().get('token')

async def main_async():
    global token1
    global token2
    await asyncio.gather(SET_LOCALE(server+token1),SET_LOCALE(server+token2))
        
asyncio.run(main_async())
