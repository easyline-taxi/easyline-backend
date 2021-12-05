import asyncio
from websockets import connect
import json
from time import sleep
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
server = 'ws://127.0.0.1:8000/ws/row/?authorization=Bearer%20'
async def main_async():
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2LCJ1c2VybmFtZSI6Im15VGVzdGVybW90b3Jpc3RhMkBnbWFpbC5jb20iLCJleHAiOjE2Mzg4NDAzNzQsImVtYWlsIjoibXlUZXN0ZXJtb3RvcmlzdGEyQGdtYWlsLmNvbSIsIm9yaWdfaWF0IjoxNjM4NjY3NTc0fQ.mYa4ahrXwDyNLjgCIgM3zVJmXBSRg6Zv1JT9GibvTx0'
    token2 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6Im15VGVzdGVybW90b3Jpc3RhMUBnbWFpbC5jb20iLCJleHAiOjE2Mzg4NDAzNzMsImVtYWlsIjoibXlUZXN0ZXJtb3RvcmlzdGExQGdtYWlsLmNvbSIsIm9yaWdfaWF0IjoxNjM4NjY3NTczfQ.8PAYI2eSZjlUJ1yhGKvd9KujCiL10ZwUK6wZojr7CWM'

    await asyncio.gather(SET_LOCALE(server+token),SET_LOCALE(server+token2))
        
asyncio.run(main_async())
