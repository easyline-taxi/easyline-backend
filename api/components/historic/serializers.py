from api import models
from rest_framework import serializers
from api.components.user.serializers import UserSerializer
class UserHistoricSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HistoricUser
        exclude = ['suject','user']
