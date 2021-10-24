from rest_framework import viewsets, status
from . import serializers
from django.db.models import Q
from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import action
from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry, Point as ptr, Polygon, LinearRing
import traceback
# ! Imports do APP
from api import models
from ..utils.utils import APIView,list_points,sendLogDiscord
from api.components.user import serializers as user_serializer

import logging
logger = logging.getLogger(__name__)

# class PointGerals(viewsets.ViewSet):
#     serializer_class = None

#     def list(self, request):
#         # ?: Listagem de Pontos
#         pass

#     def create(self, request):
#         # ?: Criação de Ponto
#         pass

#     def retrieve(self, request, pk=None):
#         # ?: informação dos pontos Ou Entrada no ponto
#         pass

#     def update(self, request, pk=None):
#         # ?: Atualizar um ponto
#         pass




class PointRegister(APIView):
    """
        Cria um ponto

        --
    """
    # ? TODO: Setup Tests
    serializer_class = serializers.PointRegisterSerializer

    def post(self, request, format=None):

        # ENVIO DE LOG DO BOT DISCORD
        sendLogDiscord(request)

        # ? Criar um ponto vinculado ao usuário
        serializer = serializers.PointRegisterSerializer(data=request.data)

        try:
            # ? Verifica a validade dos dados
            serializer.is_valid(raise_exception=True)

            # ? Cria o ponto
            point = models.Point.objects.create(**serializer.data,owner=request.user)

            models.HistoricPoint.objects.create(
                point=point, suject=request.user, motive="Ponto fundado", action="F")
            models.HistoricUser.objects.create(
                user=request.user, suject=request.user, motive="Criou o ponto", action="F")
            # ! find points by device id
            devices = models.DeviceId.objects.filter(user=request.user).order_by('-last_used')
            models.PointEmployee.objects.create(deviceid=devices[0], point=point, function="A")

            return Response({"message": _("Point Created"), "data": serializer.data})
        except Exception as ex:
            logger.error(traceback.format_exc())

            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class PointUserAction (APIView):

    # TODO: Setup Tests
    # ? Ações user(comum)/point

    serializer_class = serializers.PointUserActionSerializer
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.PointListSerializer
        return super().get_serializer_class()


    def get(self, request, format=None):
        """
            Pega os Pontos Relacionado ao user logado

            --
        """

        # ENVIO DE LOG DO BOT DISCORD
        sendLogDiscord(request)

        # ? Pega os pontos relacionado ao user
       
        # ! find points by device id
        device = models.DeviceId.objects.filter(user=request.user).order_by('-last_used').first()
        pontos_trabalhados = models.PointEmployee.objects.filter(deviceid=device)
        data = {"points":list(map(list_points,pontos_trabalhados))}
        logger.debug(data)
        serializer = serializers.PointListSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        return Response({"message": "Pontos Encontrados", "data": serializer.data})


    def post(self, request, format=None):
        """
            Escolhe qual ponto será trabalhado e ativado pelo usuário

            --
        """

        # ENVIO DE LOG DO BOT DISCORD
        sendLogDiscord(request)

        # ? Escolher qual ponto será trabalhado e ativado pelo usuário
        try:
            devices = models.DeviceId.objects.filter(user=request.user).order_by('-last_used')
            # ? Procura os pontos trabalhados
            ponto_selecionado = models.PointEmployee.objects.filter(deviceid=devices[0],point__id=request.data.get('id')).first()
            logger.info(ponto_selecionado)
            if ponto_selecionado:
                request.user.point_id = ponto_selecionado.point.id
                request.user.save()
                serializer = serializers.PointUserActionSerializer(data = {"point" : list_points(ponto_selecionado)})
                serializer.is_valid(raise_exception=True)
                return Response({"message": "Point Selected "+str(request.user.point_id),"data": serializer.data})
            return Response({"message": "Point does not exists " + str(request.data.get('id'))}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(ex)
            return Response({"message": "Point does not exists " + str(request.data.get('id'))}, status=status.HTTP_400_BAD_REQUEST)


# TODO listar todos os usuário do ponto

   