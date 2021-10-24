
from rest_framework import viewsets, status, exceptions
from . import serializers
from django.db.models import Q
from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import action
from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry, Point as ptr, Polygon, LinearRing

from . import permissions
import json


# ! Imports do APP
from api import models
from ..utils.utils import APIView,list_points,sendLogDiscord


import logging
logger = logging.getLogger(__name__)


class PointOwnerAction(APIView):

    permission_classes = [permissions.IsOwner]

    # TODO: Setup Tests
    serializer_class = serializers.PointOwnerActionSerializer
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PUT":
            return serializers.CoordinateSerializer
        else:
            return serializers.PointOwnerActionSerializer

    def put(self,request, format=None):
        """
            Seta as coodernadas do polygono

            __

        """
        # ENVIO DE LOG DO BOT DISCORD
        sendLogDiscord(request)

        point = models.Point.objects.get(pk=request.user.point_id)
        
        # ? Verifica se o polygono existe
        if not request.data.get('coordinates'):
            return Response({"message": "Campo 'coordinates' é necessário "},status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.CoordinateSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        # ? Verifica se o poligono tem pontos >= 2 e <=5
        if len(serializer.data.get('coordinates')) <3 and len(serializer.data.get("coordinates"))>6:
            return Response({"message": "Polígono mal formado, deve ter 3 a 5 pontos."},status=status.HTTP_400_BAD_REQUEST)

        logger.info(serializer.data.get("coordinates"))
        coords = map(lambda x: (x.get('latitude',None),x.get('longitude',None)), serializer.data.get("coordinates"))
        try:
            polygon= Polygon(tuple(coords))
        except Exception as ex:
            logger.error(ex)
            return Response({"message": "Polígono mal formado."},status=status.HTTP_400_BAD_REQUEST)

        point.local = list(serializer.data.get('coordinates'))
        point.save()
        return Response({"message": "Ponto Salvo", "data":model_to_dict(point)})

    def delete(self, request, format=None):
        """ 
            DELETAR PONTO (apenar Owner do ponto)

            --
        """
    
        # ENVIO DE LOG DO BOT DISCORD
        sendLogDiscord(request)

        # ?  Deletar o ponto
        point = models.Point.objects.get(pk=request.user.point_id)

        if point == None:
            return Response({"message": "Point is invalid " + str(request.data.get('point'))}, status=status.HTTP_400_BAD_REQUEST)
        
        device = models.DeviceId.objects.filter(user=request.user).order_by('-last_used').first()
        p = models.PointEmployee.objects.filter(
            deviceid=device, function="A", point__id = point.id).first()

        if p:
            p.point.delete()
            return Response({"message": "Point Deleted with Sucessful"})
        return Response({"message": "Você não é Administrador desse ponto: " + str(request.data.get('point'))}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        """ 
            Transferir ponto  (apenar Owner do ponto)

            --
        """
        # TODO: TESTAR

        # ENVIO DE LOG DO BOT DISCORD
        sendLogDiscord(request)


        # ? get actual point 
        point = models.Point.objects.get(pk=request.user.point_id)

        serializer = serializers.PointOwnerActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ? pega o email do usuário que ele quer transferir
        user = models.User.objects.get(email=request.data.get('email'))
        target = models.DeviceId.objects.filter(user=user).order_by('-last_used').first()

        #  ?: Verificar se o cara que ele quer transferir está no ponto
        if not models.PointEmployee.objects.filter(point=point,deviceid=target).count():
            return Response({"message": "Usuário não pertence a este ponto"},status=status.HTTP_400_BAD_REQUEST)

        # ? Trasnfere a posse
        point.owner = target.user
        point.save()

        # ? trocar as posições
        
        device = models.DeviceId.objects.filter(user=request.user).order_by('-last_used').first()
        employee = models.PointEmployee.objects.filter(point=point,deviceid=device).first()
        employee.function = "M"
        employee.save()
        employee = models.PointEmployee.objects.filter(point=point,deviceid=target).first()
        employee.function = "A"
        employee.save()

        # ? adicionar no histórico do ponto e do usuário

        models.HistoricPoint.objects.create(point=point, suject=request.user, motive="Transferência de Posse", action="T")
        models.HistoricUser.objects.create(user=request.user, suject=target.user, motive="Transferência de Posse", action="T")

        return Response({"message": "Ponto Transferido","data": model_to_dict(point)} )

class PointOwnerUserAction(APIView):
    # TODO: Setup Tests

    serializer_class = serializers.PointOwnerActionSerializer
    permission_classes = [permissions.IsOwner]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PUT":
            return serializers.RemoveUserToPoint
        else:
            return serializers.AddUserToPoint

    def post(self, request, format=None):
        """
            Adicionar usuários do ponto (apenar Owner do ponto)

            --
        """

        # ENVIO DE LOG DO BOT DISCORD
        sendLogDiscord(request)

        # ? TODO: Adicionar usuários do ponto

        #  ? checa se o usuário TEM PERMISSAO para adicionar no point
        point = models.Point.objects.get(pk = request.user.point_id)
        
        # TODO: ADicionar as limitações do ponto com base nos planos

        # TODO Verificar se o usuário já esta cadastrado 

        # ? TODO: buscar pelo device id
        serializer = serializers.AddUserToPoint(data = request.data)
        serializer.is_valid(raise_exception=True)

        try:
            device = models.DeviceId.objects.get(deviceid = serializer.data.get('deviceid'), user__email = serializer.data.get('email'))
        except Exception as ex:
            logger.error(ex)
            return Response({"message": "DeviceId do usuário é inválido."},status=status.HTTP_400_BAD_REQUEST)
        

        if models.PointEmployee.objects.filter(deviceid=device, point=point).exists():
            raise exceptions.ValidationError({"message":"Este usuário já está no ponto."})

        # ? TODO: Adicionar nos EMPLOYEEs
        models.PointEmployee.objects.create(deviceid=device, point=point, function="M")

        # ? TODO: Adicionar no histórico
        models.HistoricPoint.objects.create(point=point, suject=request.user, motive="Adicionou usuário", action="ADD")
        models.HistoricUser.objects.create(user=request.user, suject=device.user, motive="Adicionou usuário", action="ADD")

        return Response({"message": "Usuário Adicionado","data":{"email":device.user.email,"deviceid": device.deviceid}})

    
    def put(self,request,format=None):
        """ 
            Remover usuários do ponto (apenar Owner do ponto)

            --
        """

        # ENVIO DE LOG DO BOT DISCORD
        sendLogDiscord(request)

        # TODO: Setup Tests

        serializer = serializers.RemoveUserToPoint(data = request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.data.get('motive'):
            serializer.data['motive'] = "Removeu o usuário usuário"

        # ? TODO Verficiar o usuário tem permissão
        point = models.Point.objects.get(pk = request.user.point_id)
        
        # ! manda o email do cara
        device = models.DeviceId.objects.filter(deviceid=serializer.data.get("suject").get('deviceid')).order_by('-last_used').first()

        # ? TODO Verficiar se o usuário está no ponto
        
        if not len(models.PointEmployee.objects.filter(point=point,deviceid=device)):
            return Response({"message": "Usuário não pertence a este ponto"},status=status.HTTP_400_BAD_REQUEST)
        
        # ? TODO Remover o usuário
        employee = models.PointEmployee.objects.filter(point=point,deviceid=device).first()
        employee.delete()
        
        # ? TODO Adicionar nos históricos
        models.HistoricPoint.objects.create(point=point, suject=request.user, motive=serializer.data.get("motive"), action="REM")
        models.HistoricUser.objects.create(user=request.user, suject=device.user, motive=serializer.data.get("motive"), action="REM")

        return Response({"message": "Usuário Removido", "data": serializer.data})



class HistoricPOintViewSet(APIView):
    # TODO: Setup Tests

    serializer_class = serializers.PointOwnerActionSerializer
    permission_classes = [permissions.IsOwner]


    def post(self,request,format=None):
        """
            Consulta de Histórico do usuário com base no email dele

        --

        """
        serializer = serializers.PointOwnerActionSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = models.User.objects.get(**serializer.data)
        userHistoric = models.HistoricUser.objects.filter(Q(suject=user) | Q(user=user))
        logger.info(list(map(lambda x: x.__dict__ ,userHistoric)))
        data = {
            "user": user.__dict__,
            "historics":list(map(lambda x: x.__dict__ ,userHistoric))
        }
        serializer_historic = serializers.GetHistoricUserSerializer(data=data)
        serializer_historic.is_valid(raise_exception=True)
        return Response({"message": "Historico Encontrado", "data":serializer_historic.data })

