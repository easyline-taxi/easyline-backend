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
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0MCwidXNlcm5hbWUiOiJ3ZXNsZXliZW5pY2lvNEBnbWFpbC5jb20iLCJleHAiOjE2NDY2Njc4NzYsImVtYWlsIjoid2VzbGV5YmVuaWNpbzRAZ21haWwuY29tIiwib3JpZ19pYXQiOjE2NDY0OTUwNzZ9.trKJzdrPXFnt-YgvTa_39BF-bSawLyRMol6yXfNeBUA"
    sio.connect('https://websocket.easyline.ml/', namespaces=['/row'], auth=token)
    sio.emit("set_location",{"coordinate":{"latitude": 0,"longitude": 0}}, namespace="/row")
    sio.wait()
    sio.disconnect()