from rest_framework import serializers
from django.utils import timezone
from rest_framework.fields import JSONField

# ! Imports from App
from api import models
from api.components.user import serializers as user_serializer
from api.components.historic import serializers as historic_serializer

class PointRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Point
        exclude = ['owner','local']

class PointActions(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Point
        fields = ['name','plan','city','country']

class PointOwnerActionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.User
        fields = ['email']


    
class AddUserToPoint(serializers.ModelSerializer):
    deviceid = serializers.CharField()
    class Meta:
        model = models.User
        fields = ['email','deviceid']

class RemoveUserToPoint(serializers.ModelSerializer):
    suject = AddUserToPoint()
    class Meta:
        model = models.HistoricPoint
        fields = ["motive","suject"]


class PointCoordinateSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
class CoordinateSerializer(serializers.Serializer):
    coordinates = PointCoordinateSerializer(many=True)

class PointHistoricSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HistoricPoint
        fields = '__all__'


class PointSerializer(serializers.ModelSerializer):
    onlines = serializers.IntegerField(default=0)
    function = serializers.CharField(default="n")
    class Meta:
        model = models.Point
        fields = ['pk','name', "owner_id","onlines","function"]


class PointGetOwnerSerializer(serializers.ModelSerializer):
    local = serializers.JSONField()
    class Meta:
        model = models.Point
        fields = '__all__'
class PointListSerializer(serializers.Serializer):
    points = PointSerializer(many=True)


class PointUserActionSerializer(serializers.Serializer):
    point = PointSerializer()


class GetHistoricUserSerializer(serializers.Serializer):
    user = user_serializer.UserSerializer()
    historics = historic_serializer.UserHistoricSerializer(many=True)

