
import ast
from django.utils import timezone
from api import models
from django.contrib.gis.geos import Polygon, Point
from django.db.models import Q
import math
from django.core import serializers
from consumer import models as models_consumer
from api.components.admin import serializers

# Listar todas as actions habilitadas
actions_list = ['SET_LOCALE','GET_ROW']

def actions_exists(action=None):
    if action.upper() in actions_list:
        return action.upper()
    else:
        return None



def CHECK_IF_IN_POLYGON(user:models.User,params = None):
    """
    Parametros Recebidos

    - user model
    
    """

    # Está no ponto?
    in_local=False
    
    point = models.Point.objects.get(pk = user.point_id)
    if point.local:
        # pega o=poligono
        area = Polygon(point.convert_local_in_points())
        centroid = area.centroid
        
        distance = math.dist(centroid,(user.last_position.get('latitude'),user.last_position.get('longitude')))

        
        # prepara o poligono
        area = area.prepared
        
        fila = models.PointRow.objects.filter(user=user)
        # Verifica se está no ponto e nao está na fila
        print(user.convert_position_in_points())
        if area.contains(Point(user.convert_position_in_points())):
            distance = 0
            in_local = True
            if user.status == "IND":
                user.status = "DIS"
                user.save()
                models.HistoricUser.objects.create(user=user,action="ATT",suject=user,motive="Ficou Disponível (Dentro do Ponto)")

            
            if not fila:
                #Entra na fila
                row_pos = models.PointRow.objects.create(point=point,user=user,date=timezone.now(),online=True,link_with_online =models_consumer.Client.objects.get(user=user) )
                row_pos.position = row_pos.last_position()
                row_pos.save()
                # Adiciona histórico
                models.HistoricUser.objects.create(user=user,action="EP",suject=user)

                # historico do ponto
                models.HistoricPoint.objects.create(point=point,action="EP",suject=user)
            
            return {"in_local": in_local,"distance": distance,"position_row":models.PointRow.objects.get(user=user).position}
            

        else:
            in_local = False
            # Trata se está saindo do ponto ou está entrando no ponto
            if fila:
                # fora da
                user.status = "IND"
                user.save()

                models.HistoricUser.objects.create(user=user,action="ATT",suject=user,motive="Ficou Indisponível (Fora do Ponto)")
                models.HistoricPoint.objects.create(point=point,action="SP",suject=user)

                return {"in_local": in_local,"distance": distance,"position_row":models.PointRow.objects.get(user=user).position}

        return {"in_local": in_local,"distance": distance,"position_row":None}
    else:
        print("Ponto não tem localidade")
        return {"in_local": in_local,"distance": None,"position_row":None,"warning": "Point no has local"}



def SET_LOCALE(user,params):
    """
    Parametros Recebidos

    {
        "coordinate":"(1.96,4.57)"
    }
    
    """
    
    # coordinate = ast.literal_eval(params.get("coordinate"))
    serializer = serializers.PointCoordinateSerializer(data=params.get("coordinate"))
    serializer.is_valid(raise_exception=True)

    user.last_position = serializer.data
    user.last_position_time = timezone.now()
    user.save()
    response = CHECK_IF_IN_POLYGON(user)
    return {"detail": "LOCALIZAÇÃO ATUALIZADA", "response": response, "user": user.id}

def GET_ROW(user,params):
    """
    Parametros recebidos


    RETORNA A LISTA DE USUÀRIO NA FILA em real time
    """

    point = models.Point.objects.get(pk = user.point_id)
    row_pos = models.PointRow.objects.filter(point=point, user__status="DIS")
    response = serializers.serialize("json", row_pos)

    return {"detail": "usuários", "response": response, "user": user.id}
