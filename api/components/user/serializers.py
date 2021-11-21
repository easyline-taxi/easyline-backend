from rest_framework import serializers
from django.utils import timezone
from easyline.utils import genAction,genEmployee

# ! Import from App
from api import models
from api.components.point import serializers as point_serializers




class UserSerializer(serializers.HyperlinkedModelSerializer):
    cpf = serializers.CharField(read_only=True)
    class Meta:
        model = models.User
        fields = ['pk','vtr', "name","city","country","photo","email","cpf","status"]

class UserDataPoints(serializers.Serializer):
    user = UserSerializer()
    points = point_serializers.PointSerializer(many=True)

