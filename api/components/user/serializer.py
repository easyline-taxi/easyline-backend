from rest_framework import serializers
from django.utils import timezone
from easyline.utils import genAction,genEmployee

# ! Import from App
from api.models import User,Point,HistoricPoint,HistoricUser,PointEmployee

class UserSerializerPut(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['vtr', 'name',"city",'country','photo']



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['vtr', 'name',"city",'country',]
