from rest_framework import serializers
from django.utils import timezone

# ! Imports from App
from api.models import Point,User


class PointRegisterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Point
        fields = ['name','plan','city','country']

class PointActions(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Point
        fields = ['name','plan','city','country']

class PointOwnerActionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class PointUserActionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(max_length=200)
    class Meta:
        model = Point
        fields = ['id']

class PointOwnerActionSerializerPolygon(serializers.Serializer):
    coordinates = serializers.JSONField(default=[])


