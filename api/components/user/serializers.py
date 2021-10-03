from rest_framework import serializers
from django.utils import timezone
from easyline.utils import genAction,genEmployee

# ! Import from App
from api import models

class UserSerializerPut(serializers.HyperlinkedModelSerializer):
    # photo = serializers.ImageField()
    class Meta:
        model = models.User
        fields = ['vtr', "name","city","country","photo"]



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.User
        fields = ['vtr', 'name',"city",'country']


class UserHistoricSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HistoricUser
        fields = '__all__'

