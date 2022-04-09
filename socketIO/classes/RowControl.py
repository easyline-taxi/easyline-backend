import socketio
from socketio.exceptions import ConnectionRefusedError
import json
# from api import models

from api import models as api_models
import logging
from ..actions import SET_LOCALE
from socketIO import models,authentication_socket

models.ClientWebsocket.objects.all().delete()

class RowControl(socketio.Namespace):
    def on_connect(self, sid, environ,auth):
        res = api_models.Token.objects.filter(key=auth).first()
        user = authentication_socket.auth_socket(sid,auth)
        if user:
            self.save_session(sid, {'user': res.user,'point':res.user.point_id})
            self.enter_room(sid, int(res.user.point_id))
            print("Connected: ",sid)
        
    def on_send_notify(self, sid, data):
        # send row_update
        session = self.get_session(sid)
        user = session.get("user")
        user.refresh_from_db()
        print("ON SEND NOTIFY :",user)
        
        models.HistoricWebsocket.objects.create(user=session.get("user"),sid=sid,point=session.get("point"),action="row_update",complement=data)
        self.emit('row_update', {"status": 200},room=session.get("point"))
        
        
    def on_set_location(self, sid, data):
        try:
            session = self.get_session(sid)
            models.HistoricWebsocket.objects.create(user=session.get("user"),sid=sid,point=session.get("point"),action="set_location",complement=data)
            res = SET_LOCALE(session.get("user"),data)
            if res.get("response").get("update"):
                models.HistoricWebsocket.objects.create(user=session.get("user"),sid=sid,point=session.get("point"),action="row_update",complement=data)
                self.emit('row_update', {"status": 200, "data": res},room=session.get("point"))
            self.emit('location_updated', {"status": 200, "data": res})
        except Exception as ex:
            logging.error(ex)
            models.HistoricWebsocket.objects.create(user=session.get("user"),sid=sid,point=session.get("point"),action=str(ex))

    def on_disconnect(self, sid):
        print('disconnect ', sid)
        session = self.get_session(sid)
        if session.get("user"):
            models.ClientWebsocket.objects.filter(user=session.get("user"),sid=sid).delete()
            self.leave_room(sid, int(session.get("point")))

    
        
