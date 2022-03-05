from django.utils import timezone
from api import models
from django.contrib.gis.geos import Polygon, Point
from django.db.models import Q
import math
from django.core import serializers as djserializers
from api.components.admin import serializers
from . import CHECK_IF_IN_POLYGON

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
    user.refresh_from_db()
    user.last_position = serializer.data
    user.last_position_time = timezone.now()
    user.save()
    response = CHECK_IF_IN_POLYGON(user)
    return {"detail": "LOCATION_UPDATED", "response": response, "user": user.id}