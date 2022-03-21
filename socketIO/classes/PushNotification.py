import socketio
from socketio.exceptions import ConnectionRefusedError
import json

from api import models as api_models
import logging
from socketIO import models
from socketIO import models,authentication_socket

class PushNotification(socketio.Namespace):
    
    def on_connect(self, sid, environ,auth):
        res = api_models.Token.objects.filter(key=auth).first()
        user = authentication_socket.auth_socket(sid,auth)
        if user:
            self.save_session(sid, {'user': res.user,'point':res.user.point_id})
            self.enter_room(sid, int(res.user.point_id))
            print("Connected Notifications: ",sid)
    
    def on_send_notify(self, sid, data):
        # send row_update
        session = self.get_session(sid)
        user = session.get("user")
        user.refresh_from_db()
        models.HistoricWebsocket.objects.create(user=session.get("user"),sid=sid,point=session.get("point"),action="notification_update",complement=data)
        self.emit('notification_update', {"status": 200},room=session.get("point"))
    
    def on_disconnect(self, sid):
        print("Disconnected Notifications: ",sid)
        session = self.get_session(sid)
        if session.get("user"):
            models.ClientWebsocket.objects.filter(user=session.get("user"),sid=sid).delete()
            self.leave_room(sid, int(session.get("point")))

    