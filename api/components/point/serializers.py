from rest_framework import serializers
from django.utils import timezone

# ! Imports from App
from api import models


class PointRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Point
        exclude = ['owner','local']

class PointSerializer(serializers.ModelSerializer):
    onlines = serializers.IntegerField(default=0)
    function = serializers.CharField(default="n")
    class Meta:
        model = models.Point
        fields = ['pk','name', "owner_id","onlines","function"]

class PointListSerializer(serializers.Serializer):
    points = PointSerializer(many=True)


class PointUserActionSerializer(serializers.Serializer):
    point = PointSerializer()

