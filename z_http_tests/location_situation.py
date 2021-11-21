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

async def main_async():
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2LCJ1c2VybmFtZSI6Im15VGVzdGVybW90b3Jpc3RhMkBnbWFpbC5jb20iLCJleHAiOjE2Mzc2NzcxMjcsImVtYWlsIjoibXlUZXN0ZXJtb3RvcmlzdGEyQGdtYWlsLmNvbSIsIm9yaWdfaWF0IjoxNjM3NTA0MzI3fQ.4F61yBlVxrNudc4ZivKTCYn1Utc4LL1hg6OGBkogFqU'
    token2 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6Im15VGVzdGVybW90b3Jpc3RhMUBnbWFpbC5jb20iLCJleHAiOjE2Mzc2NzcxMjYsImVtYWlsIjoibXlUZXN0ZXJtb3RvcmlzdGExQGdtYWlsLmNvbSIsIm9yaWdfaWF0IjoxNjM3NTA0MzI2fQ.6xy95OmNVcVy1_bqi-rKroL0AASv1h0ISJBoSFCLolA'

    await asyncio.gather(SET_LOCALE("ws://127.0.0.1:8000/ws/row/?authorization=Bearer%20"+token),SET_LOCALE("ws://127.0.0.1:8000/ws/row/?authorization=Bearer%20"+token2))
        
asyncio.run(main_async())
