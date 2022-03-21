
import os
import sys
import json
from dotenv import dotenv_values
config = dotenv_values('.env')

#mark django settings module as settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "easyline.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import eventlet
import socketio
from socketIO.classes import RowControl,PushNotification


# create a Socket.IO server
sio = socketio.Server(logger=False,async_mode='eventlet')

# wrap with a WSGI application
app = socketio.WSGIApp(sio)

sio.register_namespace(RowControl('/row'))
sio.register_namespace(PushNotification('/notification'))

@sio.on('*')
def catch_all(event, sid, data):
    print('O Evento '+event+' Não Existe')
    sio.emit(json.dumps({"status":404, "data": 'O Evento '+event+' Não Existe'}))
instance = None
if __name__ == '__main__':
    print("Servidor Startando ")
    instance = eventlet.wsgi.server(eventlet.listen(('', int(config.get('PORT_WEBSOCKET')))), app)
    