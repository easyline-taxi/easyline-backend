from rest_framework import serializers
from django.utils import timezone

# ! Imports from App
from api.models import Point

class PointGeralSerializer(serializers.HyperlinkedModelSerializer):
    pass

class PointRegisterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Point
        fields = ['name','plan','city','country']