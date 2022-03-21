import socketio
import time
from api import models
from django.conf import settings


def send_row(user):
    url = "http://"+settings.SOCKET_IO_SETTINGS.get("url")+":"+str(settings.SOCKET_IO_SETTINGS.get("port"))
    print("SEND ROW")
    sio = socketio.Client(reconnection=False,logger=True, engineio_logger=True)
    try:
        token = models.Token.objects.get(user=user)
        sio.connect(url,namespaces=['/row'], auth=token.key)
        
        sio.emit("send_notify",{}, namespace="/row")
        
        sio.disconnect()
    except Exception as ex:
        print("Erro Send Row - ", ex)
        
def send_notification(user):
    url = "http://"+settings.SOCKET_IO_SETTINGS.get("url")+":"+str(settings.SOCKET_IO_SETTINGS.get("port"))
    print("SEND NOTIFICATION")
    sio = socketio.Client(reconnection=False,logger=True, engineio_logger=True)
    try:
        token = models.Token.objects.get(user=user)
        sio.connect(url,namespaces=['/notification'], auth=token.key)
        
        sio.emit("send_notify",{}, namespace="/notification")
        
        sio.disconnect()
    except Exception as ex:
        print("Erro Send Row - ", ex)
    