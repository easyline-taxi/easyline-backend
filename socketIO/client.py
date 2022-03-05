import socketio
sio = socketio.Client()

@sio.event
def connect():
    print('connection established')


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

    

if __name__ == '__main__':
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6Indlc2xleWJlbmljaW80QGdtYWlsLmNvbSIsImV4cCI6MTY0NjU0NDM5MSwiZW1haWwiOiJ3ZXNsZXliZW5pY2lvNEBnbWFpbC5jb20iLCJvcmlnX2lhdCI6MTY0NjM3MTU5MX0.RZFwlkj5aeoo4bdUrdPzADjnCA1Z6IcK35DwGF7tEAg"
    sio.connect('http://127.0.0.1:8888/', namespaces=['/row'], auth=token)
    sio.emit("set_location",{"coordinate":{"latitude": 0,"longitude": 0}}, namespace="/row")
    # sio.wait()
    sio.disconnect()