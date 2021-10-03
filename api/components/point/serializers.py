from rest_framework import serializers
from django.utils import timezone

# ! Imports from App
from api import models


class PointRegisterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Point
        fields = ['name','plan','city','country']

class PointActions(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Point
        fields = ['name','plan','city','country']

class PointOwnerActionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.User
        fields = ['email']

class PointUserActionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(max_length=200)
    class Meta:
        model = models.Point
        fields = ['id']

class PointOwnerActionSerializerPolygon(serializers.Serializer):
    coordinates = serializers.JSONField(default=[])

class PointHistoricSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HistoricPoint
        fields = '__all__'


