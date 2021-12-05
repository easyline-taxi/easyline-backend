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
server = 'ws://easyline.ml:8000/ws/row/?authorization=Bearer%20'

async def main_async():
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNCwidXNlcm5hbWUiOiJteVRlc3Rlcm1vdG9yaXN0YTJAZ21haWwuY29tIiwiZXhwIjoxNjM4ODQwMzcyLCJlbWFpbCI6Im15VGVzdGVybW90b3Jpc3RhMkBnbWFpbC5jb20iLCJvcmlnX2lhdCI6MTYzODY2NzU3Mn0.JbYyNb_mFy4zDy1Xvg9f1okdplWg5047L_hH_fhOALk'
    token2 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMywidXNlcm5hbWUiOiJteVRlc3Rlcm1vdG9yaXN0YTFAZ21haWwuY29tIiwiZXhwIjoxNjM4ODQwMzcxLCJlbWFpbCI6Im15VGVzdGVybW90b3Jpc3RhMUBnbWFpbC5jb20iLCJvcmlnX2lhdCI6MTYzODY2NzU3MX0.ChEVztLuQnKKHCt4iI4BD5Fe3cKt5Naa2GTh14Jwi-Y'
    await asyncio.gather(SET_LOCALE(server+token),SET_LOCALE(server+token2))
        
asyncio.run(main_async())
