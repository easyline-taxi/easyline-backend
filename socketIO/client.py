import socketio
import time
sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.on('connect', namespace='/row')
def connect():
    print('connection established namespace')


@sio.on('my_message',namespace='/row')
def on_message(data):
    print('I received a message!', data)        

@sio.on('location_updated',namespace='/row')
def on_message(data):
    print('POSIÇÂO alterada!', data)       
    

@sio.on('row_update',namespace='/row')
def on_message(data):
    print('FILA alterada ', data)    
    

@sio.event(namespace='/row')
def connect_error(data):
    print("The connection failed!",data)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

@sio.event
def disconnect():
    print('disconnected from server')

    
url = "http://127.0.0.1:8888"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6Indlc2xleWJlbmljaW80QGdtYWlsLmNvbSIsImV4cCI6MTY0NzkxMjYzMCwiZW1haWwiOiJ3ZXNsZXliZW5pY2lvNEBnbWFpbC5jb20iLCJvcmlnX2lhdCI6MTY0NzczOTgzMH0.BEIaAlmAuGv6mg7eTaRK5RUH07NJR-z7kAOlIEFToQk"

if __name__ == '__main__':
    sio.connect(url,namespaces=['/row'], auth=token)
    while True:
        try:
            sio.emit("set_location",{"coordinate":{"latitude": 0,"longitude": 0}}, namespace="/row")
            # sio.emit("send_notify",{"coordinate":{"latitude": 0,"longitude": 0}}, namespace="/row")
            time.sleep(5)
        except Exception:
            print("reconnectando")
            try:
                sio.connect(url, namespaces=['/row'],auth=token)
            except:
                print("Falhou")
                pass
    sio.wait()