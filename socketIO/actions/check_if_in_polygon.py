from django.utils import timezone
from api import models
from django.contrib.gis.geos import Polygon, Point
from django.db.models import Q
import math
from django.core import serializers as djserializers
from api.components.admin import serializers


def CHECK_IF_IN_POLYGON(user:models.User,params = None):
    """
    Parametros Recebidos

    - user model
    
    """
    # Está no ponto?
    in_local=False
    
    user.refresh_from_db()
    point = models.Point.objects.get(pk = user.point_id)
    
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
                models.HistoricUser.objects.create(user=user,action="ATT",suject=user,motive="Entrou na Fila")
                
                row_pos = models.PointRow.objects.create(point=point,user=user,date=timezone.now())
                if not row_pos.position:
                    row_pos.position = row_pos.last_position()
                    row_pos.save()
                                
                models.HistoricPoint.objects.create(point=point,action="EP",motive="Entrou no Ponto!",suject=user)
                return {"in_local": in_local,"distance": distance,"update": True,"position_row": row_pos.position if row_pos else None }
                
                
            row_user = models.PointRow.objects.filter(point=point,user=user).first()
            return {"in_local": in_local,"distance": distance,"position_row": row_user.position if row_user else None }
            
        else:
            in_local = False            
            if fila and user.status == "DIS" :
                models.HistoricPoint.objects.create(point=point,action="SP",motive="Saiu do Ponto",suject=user)

            row_user = models.PointRow.objects.filter(point=point,user=user).first()
            return {"in_local": in_local,"distance": distance,"position_row": row_user.position if row_user else None }
    else:
        print("Ponto não tem localidade")
        return {"in_local": in_local,"distance": None,"position_row":None,"warning": "Point no has local"}