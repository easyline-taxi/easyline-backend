
from rest_framework import viewsets, status,exceptions
from django.utils.translation import gettext as _
from rest_framework.response import Response
from . import serializers
import base64
import io
from PIL import Image

# ! Import From App
from api import models
from ..utils.utils import APIView,list_points,sendLogDiscord

import re

import logging
logger = logging.getLogger(__name__)


def normalize_base64(photo_b64:str):
    if not photo_b64:
        return None

    if photo_b64.startswith('data:'):
        re_b64 = re.compile(r'data:image\/[a-z]+;base64,')
        b64_header = re_b64.findall(photo_b64)
        type_file_b64 = b64_header[0].split(';')[0].split('/')[1]
        photo_b64 = re.sub(r'data:image\/[a-z]+;base64,', "",photo_b64)
    try:
        image = Image.open(io.BytesIO(base64.b64decode(photo_b64)))
    except Exception as ex:
        raise exceptions.ValidationError("Imagem incorret format")

    # ?get image size
    (width, height) = image.size 
    if width > 70 or height > 70:
        # ? Resize Image
        image = image.resize((70,70), Image.ANTIALIAS)

    # ?Convert do base64
    output = io.BytesIO()
    image.save(output, format=type_file_b64)
    b64 = base64.b64encode(output.getvalue()).decode('utf-8')
    b64image = b64_header[0]+b64
    return b64image

class UserDataView(APIView):

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PUT":
            return serializers.UserSerializer
        else:
            return serializers.UserDataPoints
        
    def get(self, request, format=None):
        """
            Retorna os dados referentes ao usuário
        """

        # ENVIO DE LOG DO BOT DISCORD
        sendLogDiscord(request)

        #  ?: Retorna os dados do usuário

        # ? Verifica se o deviceId é correspondente ao usuário
        
        # if not len(DeviceId.objects.filter(deviceid=request.user.deviceid)):
        #     # ! se não tiver device id registrado neste user REGISTRAR OUTRO DEVICE ID NELE
        #     return Response({"message": "DeviceId Invalid"}, status=status.HTTP_401_UNAUTHORIZED)  
        
        device = models.DeviceId.objects.filter(user=request.user).order_by('-last_used').first()

        # ? Procura os pontos trabalhados
        pontos_trabalhados = models.PointEmployee.objects.filter(deviceid=device,deviceid__user=request.user)
        
        
        data = {
            "user": request.user.__dict__,
            "points": list(map(list_points,pontos_trabalhados))
        }
        serializer = serializers.UserDataPoints(data=data)
        serializer.is_valid(raise_exception=True)

        try:

            # ? get image
            b64image = normalize_base64(request.user.photo)
            request.user.photo = b64image
            request.user.save()
        except Exception as ex:
            logger.error(ex)

        return Response({"data":serializer.data})

    def put(self,request, format=None):
        """
             Atualiza os dados do usuário
        """
        
        # ? Verifica se o deviceId é correspondente ao usuário
        # ! Não precisa mais verificar deviceID
        # if not str(request.user.deviceid) == str(request.data.get('deviceid')):
        #     return Response({"message": "DeviceId Invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        # ENVIO DE LOG DO BOT DISCORD
        sendLogDiscord(request)


        if request.data.get('photo'):
            request.data['photo'] = normalize_base64(request.data.get('photo'))
        # ? Aloca os campos necessários de acordo com o modelo 
        serializer = serializers.UserSerializer(request.user,data =request.data)
        try:
            # ? Verifica a validade dos campos
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # ? TODO: ADicionar no HIstorico do Usuário essas ALTERÇÔES
            models.HistoricUser.objects.create(user=request.user, suject=request.user,action="ATT",motive="atualização")

            return Response({"message":"Update Sucessful" , "data":serializer.data})
        except Exception as ex:
            logger.error(ex)
            # ? Senão retorna erro 404
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,format=None):
        """
            # ?: Deleta o usuário

            --
            
        """
        # ?: Deleta o usuário
        # ! Verificar a validade disso, pois acho que a conta não poderá ser excluida

        # ENVIO DE LOG DO BOT DISCORD
        sendLogDiscord(request)
            
        try:
            request.user.delete()
            return Response({"message":"Deleted Sucessful"})
        except Exception as ex:
            logger.error(ex)
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
