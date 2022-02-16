from rest_framework import viewsets, status,exceptions
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
from ..utils import utils
from api.components.user import serializers as user_serializer
# TEsta dps
# from django.contrib.auth.decorators import user_passes_test

# def point_check(user):
#     device = models.DeviceId.objects.filter(user=user).order_by('-last_used').first()
#     pontos_trabalhados = models.PointEmployee.objects.filter(deviceid=device)
#     return True if pontos_trabalhados.filter(point=user.point_id) else False

import logging

logger = logging.getLogger(__name__)

class PointRegister(utils.APIView):
    """
        Cria um ponto

        --
    """
    # ? TODO: Setup Tests
    serializer_class = serializers.PointRegisterSerializer

    def post(self, request, format=None):

        # ENVIO DE LOG DO BOT DISCORD
        utils.sendLogDiscord(request)

        # ? Criar um ponto vinculado ao usuário
        serializer = serializers.PointRegisterSerializer(data=request.data)

        try:
            # ? Verifica a validade dos dados
            serializer.is_valid(raise_exception=True)

            # ? Cria o ponto
            point = models.Point.objects.create(**serializer.data, owner=request.user)

            models.HistoricPoint.objects.create(
                point=point, suject=request.user, motive="Ponto fundado", action="F")
            models.HistoricUser.objects.create(
                user=request.user, suject=request.user, motive="Criou o ponto", action="F")
            # ! find points by device id
            device = models.DeviceId.objects.filter(user=request.user).order_by('-last_used').first()
            if not device:
                raise exceptions.NotAcceptable("Usuário (id: {}) não possui deviceId Registrado.".format(request.user.id))
            models.PointEmployee.objects.create(deviceid=device, point=point, function="A")

            return Response({"message": _("Point Created"), "data": model_to_dict(point)})
        except Exception as ex:
            logger.error(traceback.format_exc())

            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class PointUserAction(utils.APIView):
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
        utils.sendLogDiscord(request)

        # ? Pega os pontos relacionado ao user

        # ! find points by device id
        pontos_trabalhados = utils.pontosTrabalhados(request.user)
        data = {"points": list(map(utils.list_points, pontos_trabalhados))}
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
        utils.sendLogDiscord(request)

        # ? Escolher qual ponto será trabalhado e ativado pelo usuário
        
        # ? Procura os pontos trabalhados
        serializer = serializers.PointUserActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Pega o ponto selecionado e traz caso não ocorra uma exception
        ponto_selecionado = utils.pontosTrabalhados(request.user,serializer.data.get('point',-1))
        
        if ponto_selecionado:
            request.user.point_id = ponto_selecionado.point.id
            request.user.save()
            return Response({"message": "Point Selected " + str(request.user.point_id), "data": serializer.data})
        return Response({"detail": "Point does not exists " + str(request.data.get('id')), "data": serializer.data},
                        status=status.HTTP_400_BAD_REQUEST)
    
# TODO listar todos os usuário do ponto

class PointRowAction(utils.APIView):
    """
        Ações relacionadas a manipulação da fila
    
        --
    """
    # TODO: Setup Tests
    # ? Ações user(comum)/point

    serializer_class = serializers.PointRowUserActionSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.GETPointRowUserActionSerializer
        if self.request.method == "PUT":
            return serializers.PUTPointRowUserActionSerializer

        return super().get_serializer_class()
    
    def get(self, request, format=None):
        """
            Pega os dados da fila

            --
        """

        # ENVIO DE LOG DO BOT DISCORD
        utils.sendLogDiscord(request)

        # ? Pega os pontos relacionado ao user
        
        # ! find points by device id
        point = utils.pontosTrabalhados(request.user,point_id=request.user.point_id).point
        
        fila = models.PointRow.objects.filter(point=point).values()
        
        for motorista in fila:
            usuario = models.User.objects.get(id= motorista.get('user_id'))
            status_moto = usuario.status
            motorista['status']= status_moto
            motorista['user'] = {
                "name": usuario.name,
                "vtr": usuario.vtr,
                "photo": usuario.photo,
            }
        
        print(fila)
        return Response({"message": "Fila Encontrada", "data": fila})

    def post(self, request, format=None):
        """
            Tripula o usuário (> prancheteiro )

            --
        """
        utils.sendLogDiscord(request)
        # ! find points by device id
        
        point_trab = utils.pontosTrabalhados(request.user,request.user.point_id)

        # ! Permission
        if point_trab.function == 'M':
            raise exceptions.PermissionDenied("Não tem autoriazação")
        
        # ? verifica se está na fila
        point = point_trab.point
        serializer = serializers.PointRowUserActionSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = models.User.objects.get(id = serializer.data.get('user'))
            objeto_fila = models.PointRow.objects.get(user=user,point=point)
            user.status = "TRI"
            user.save()
            objeto_fila.delete()
            
            models.HistoricPoint.objects.create(
                point=point, suject=user, motive="Tripulado", action="TRI")
            models.HistoricUser.objects.create(
                user=request.user, suject=user, motive="Tripulado", action="TRI")
            
        except Exception as ex:
            logger.warning(ex)
            raise exceptions.NotFound("Usuário com id {} não está na fila".format(serializer.data.get('user')))
        
    
        return Response({"message": "Usuário Tripulado com sucesso"})


    def put(self, request, format=None):
        """
            Movimenta o usuário na fila  (> prancheteiro )

            --
        """
        utils.sendLogDiscord(request)
        
        point_trab = utils.pontosTrabalhados(request.user, request.user.point_id)

        # ! Permission
        if point_trab.function == 'M':
            raise exceptions.PermissionDenied("Não tem autoriazação")
        
        serializer = serializers.PUTPointRowUserActionSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        

        try:
            user = models.User.objects.get(id = serializer.data.get('user'))
            objeto_fila = models.PointRow.objects.get(user=user,point=point_trab.point)
            
            if objeto_fila.position >= serializer.data.get('position'):
                aux_action = 'MC'
                aux_motive = 'Movido para Cima'
            else:
                aux_action = 'MB'
                aux_motive = 'Movido para Baixo'
                
           
            
        except Exception as ex:
            logger.warning(ex)
            raise exceptions.NotFound("Usuário com id {} não está na fila.".format(serializer.data.get('user')))
        
        objeto_fila.move_position(position=serializer.data.get('position'))
            
        models.HistoricPoint.objects.create(
            point=point_trab.point, suject=user, motive=aux_motive, action=aux_action)
        models.HistoricUser.objects.create(
            user=request.user, suject=user, motive=aux_motive, action=aux_action)
    
        return Response({"message": "Usuário {} Movido com sucesso.".format(serializer.data.get('user'))})
        
    
