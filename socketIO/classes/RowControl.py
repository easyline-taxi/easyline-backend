import socketio
from socketio.exceptions import ConnectionRefusedError
import json
# from api import models

from api import models as api_models
import logging
from ..actions import SET_LOCALE
from socketIO import models

models.ClientWebsocket.objects.all().delete()
class RowControl(socketio.Namespace):
    def on_connect(self, sid, environ,auth):
        
        res = api_models.Token.objects.filter(key=auth).first()
        if res and res.is_valid():            
            if res.user.point_id and res.user.point_id > 0:
                user ,exist = models.ClientWebsocket.objects.get_or_create(user=res.user,sid=sid,point=res.user.point_id)
                models.HistoricWebsocket.objects.create(user=res.user,sid=sid,point=res.user.point_id,action="connected websocket")
                self.save_session(sid, {'user': res.user,'point':res.user.point_id})
                self.enter_room(sid, res.user.point_id)
            else:
                raise ConnectionRefusedError("Sem ponto Conectado!")
        elif res:
            print("Err: Tem token - expirado")
            models.HistoricWebsocket.objects.create(user=res.user,sid=sid,point=res.user.point_id,action="failed connect")
            raise ConnectionRefusedError("Token Expirado!")
        else:
            print("Err: Sem token")
            models.HistoricWebsocket.objects.create(sid=sid,action="failed connect - sem token válido")
            raise ConnectionRefusedError("Não Autenticado!")
        
        
    def on_set_location(self, sid, data):
        try:
            session = self.get_session(sid)
            models.HistoricWebsocket.objects.create(user=session.get("user"),sid=sid,point=session.get("point"),action="send set_location",complement=data)
            res = SET_LOCALE(session.get("user"),data)
            if res.get("response").get("update"):
                models.HistoricWebsocket.objects.create(user=session.get("user"),sid=sid,point=session.get("point"),action="receive row_update",complement=data)
                self.emit('row_update', {"status": 200, "data": res},room=session.get("point"))
            models.HistoricWebsocket.objects.create(user=session.get("user"),sid=sid,point=session.get("point"),action="receive location_updated",complement=data)
            self.emit('location_updated', {"status": 200, "data": res})
        except Exception as ex:
            models.HistoricWebsocket.objects.create(user=session.get("user"),sid=sid,point=session.get("point"),action=str(ex))

    def on_disconnect(self, sid):
        print('disconnect ', sid)
        session = self.get_session(sid)
        if session.get("user"):
            models.ClientWebsocket.objects.filter(user=session.get("user")).delete()
            self.leave_room(sid, session.get("point"))

    
        
