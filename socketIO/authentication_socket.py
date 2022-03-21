

from api import models as api_models
from socketIO import models
from django.core.cache import cache # This is the memcache cache.

def auth_socket(sid,auth):
    res = api_models.Token.objects.filter(key=auth).first()
    if res and res.is_valid():            
        if res.user.point_id and res.user.point_id > 0:
            try:
                # client = models.ClientWebsocket.objects.filter(user=res.user,point=res.user.point_id)
                # client.delete()
                client = models.ClientWebsocket.objects.create(user=res.user,sid=sid,point=res.user.point_id)
                models.HistoricWebsocket.objects.create(user=res.user,sid=sid,point=res.user.point_id,action="connected websocket")
                return client
            except Exception as ex:
                models.ClientWebsocket.objects.filter(user=res.user).delete()
                raise ConnectionRefusedError(ex)
        else:
            raise ConnectionRefusedError("Sem ponto Conectado!")
    elif res:
        print("Err: Tem token - expirado")
        models.HistoricWebsocket.objects.create(user=res.user,sid=sid,point=res.user.point_id,action="failed connect unregistred token")
        raise ConnectionRefusedError("Token Expirado!")
    else:
        print("Err: Sem token")
        models.HistoricWebsocket.objects.create(sid=sid,action="failed connect - sem token válido")
        raise ConnectionRefusedError("Não Autenticado!")