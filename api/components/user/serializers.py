from rest_framework import serializers
from django.utils import timezone
from easyline.utils import genAction,genEmployee

# ! Import from App
from api import models
from api.components.point import serializers as point_serializers




class UserSerializer(serializers.HyperlinkedModelSerializer):
    cpf = serializers.CharField(required=False)
    id = serializers.IntegerField(required=False)
    class Meta:
        model = models.User
        fields = ['id','vtr', "name","city","country","photo","email","cpf","status"]

class UserDataPoints(serializers.Serializer):
    user = UserSerializer()
    points = point_serializers.PointSerializer(many=True)

