
from api import models
from . import serializers
from django.db.models import Q
from rest_framework import viewsets

class HistoricUserViewSet(viewsets.ModelViewSet):
    """
        Consulta de Histórico do Usuário (Todas as ações realizadas pelo usuário )

        --

    """
    serializer_class = serializers.UserHistoricSerializer
    queryset = models.HistoricUser.objects.all()
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user
        return models.HistoricUser.objects.filter(Q(suject=user) | Q(user=user))