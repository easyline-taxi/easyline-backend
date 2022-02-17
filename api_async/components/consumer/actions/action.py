
from django.utils import timezone
from api import models
from django.contrib.gis.geos import Polygon, Point
from django.db.models import Q
import math
from django.core import serializers as djserializers
from api.components.admin import serializers


# Listar todas as actions habilitadas
actions_list = ['SET_LOCALE']

#  ok FAZER A PARTE DE EVENTOS DE ATUALIZAÇÂO

def actions_exists(action=None):
    if action.upper() in actions_list:
        return action.upper()
    else:
        return None

def OFFILINE_POINT_ROW(user:models.User,params = None):
    user.status = "IND"
    user.save()
    
def ONLINE_POINT_ROW(user:models.User,params = None):
    if user.status != "TRI":
        user.status = "DIS"
        user.save()


def CHECK_IF_IN_POLYGON(user:models.User,params = None):
    """
    Parametros Recebidos

    - user model
    
    """

    # Está no ponto?
    in_local=False
    
    point = models.Point.objects.get(pk = user.point_id)
    user = models.User.objects.get(pk = user.id)
    if point.local:
        # pega o=poligono
        area = Polygon(point.convert_local_in_points())
        centroid = area.centroid
        
        distance = math.dist(centroid,(user.last_position.get('latitude'),user.last_position.get('longitude')))

        
        # prepara o poligono
        area = area.prepared
        
        fila = models.PointRow.objects.filter(user=user,point=point).first()
        # Verifica se está no ponto e nao está na fila
        if area.contains(Point(user.convert_position_in_points())):
            distance = 0
            in_local = True
            if user.status == "DIS" and not fila:
                models.HistoricUser.objects.create(user=user,action="ATT",suject=user,motive="Ficou Disponível (Dentro do Ponto)")
                #Entra na fila
                row_pos = models.PointRow.objects.create(point=point,user=user,date=timezone.now())
                if not row_pos.position:
                    row_pos.position = row_pos.last_position()
                    row_pos.save()
                
                # Adiciona histórico
                models.HistoricUser.objects.create(user=user,action="EP",suject=user)

                # historico do ponto
                models.HistoricPoint.objects.create(point=point,action="EP",suject=user)
            row_user = models.PointRow.objects.filter(point=point,user=user).first()
            
            return {"in_local": in_local,"distance": distance,"position_row": row_user.position if row_user else None }
            

        else:
            in_local = False
            
            # Trata se está saindo do ponto ou está entrando no ponto
            if fila:

                models.HistoricUser.objects.create(user=user,action="ATT",suject=user,motive="Ficou Indisponível (Fora do Ponto)")
                models.HistoricPoint.objects.create(point=point,action="SP",suject=user)

            row_user = models.PointRow.objects.filter(point=point,user=user).first()
            return {"in_local": in_local,"distance": distance,"position_row": row_user.position if row_user else None }
    else:
        print("Ponto não tem localidade")
        return {"in_local": in_local,"distance": None,"position_row":None,"warning": "Point no has local"}



def SET_LOCALE(user,params):
    """
    Parametros Recebidos

    {
        "coordinate":{
            "latitude": 0,
            "longitude": 0
        }
    }
    
    """
    
    # coordinate = ast.literal_eval(params.get("coordinate"))
    serializer = serializers.PointCoordinateSerializer(data=params.get("coordinate"))
    serializer.is_valid(raise_exception=True)

    user.last_position = serializer.data
    user.last_position_time = timezone.now()
    user.save()
    response = CHECK_IF_IN_POLYGON(user)
    return {"detail": "LOCATION_UPDATED", "response": response, "user": user.id}

def GET_ROW(user,params):
    """
    Parametros recebidos


    RETORNA A LISTA DE USUÀRIO NA FILA em real time
    """

    point = models.Point.objects.get(pk = user.point_id)
    row_pos = models.PointRow.objects.filter(point=point, user__status="DIS")
    response = djserializers.serialize("json", row_pos)

    return {"detail": "usuários", "response": response, "user": user.id}
