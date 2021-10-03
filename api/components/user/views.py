from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status, mixins
from django.utils.translation import gettext as _
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q
from . import serializers
import base64
import io
from PIL import Image

# ! Import From App
from api import models
from ..utils.utils import APIView


from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

    
class UserDataView(APIView):

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PUT":
            return serializers.UserSerializerPut
        else:
            return serializers.UserSerializer
        
    def get(self, request, format=None):
        """
            Retorna os dados referentes ao usuário
        """

        # ENVIO DE LOG DO BOT DISCORD
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)('background-task', {
            'type': 'send_message_discord', 
            'user': request.user.email,
            'action': request.method,
            'from':request.META.get('REMOTE_ADDR'),
            'url': request.get_full_path()
            })

        #  ?: Retorna os dados do usuário

        # ? Verifica se o deviceId é correspondente ao usuário
        
        # if not len(DeviceId.objects.filter(deviceid=request.user.deviceid)):
        #     # ! se não tiver device id registrado neste user REGISTRAR OUTRO DEVICE ID NELE
        #     return Response({"message": "DeviceId Invalid"}, status=status.HTTP_401_UNAUTHORIZED)  
        
        device = models.DeviceId.objects.filter(user=request.user).order_by('-last_used')[0]
        # ? Procura os pontos trabalhados
        pontos_trabalhados = models.PointEmployee.objects.filter(deviceid=device)
        pontos_trabalhados = [x for x in pontos_trabalhados if x.deviceid.user == request.user]

        try:

            # ? get image
            data = base64.b64decode(request.user.photo)
            image = Image.open(io.StringIO(request.user.photo))

            
            # ?get image size
            (width, height) = image.size 
            if width > 70 or height > 70:

                # ? Resize Image
                image = image.resize((70,70), Image.ANTIALIAS)

            # ?Convert do base64
            output = io.BytesIO()
            image.save(output, format=image.format)
            b64 = base64.b64encode(output.getvalue()).decode('utf-8')
            b64image = "data:image/"+image.format+";base64,"+b64
            request.user.photo = b64image
            request.user.save()
        except Exception as ex:
            pass

        
        return Response({
            "user_data":
                {
                    "id":request.user.id,
                    "vtr":request.user.vtr,
                    "name":request.user.name,
                    "email":request.user.email,
                    "photo":request.user.photo
                },
            "point_data": [
                {
                    "id":x.point.id,
                    "name":x.point.name,
                    "owner_id": x.point.owner.id,
                    "onlines":models.PointEmployee.objects.all().filter(point=x.point).count(),
                    "function": x.function
                } for x in pontos_trabalhados]})

    def put(self,request, format=None):
        """
             Atualiza os dados do usuário
        """
        
        # ? Verifica se o deviceId é correspondente ao usuário
        # ! Não precisa mais verificar deviceID
        # if not str(request.user.deviceid) == str(request.data.get('deviceid')):
        #     return Response({"message": "DeviceId Invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        # ENVIO DE LOG DO BOT DISCORD
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)('background-task', {
            'type': 'send_message_discord', 
            'user': request.user.email,
            'action': request.method,
            'from':request.META.get('REMOTE_ADDR'),
            'url': request.get_full_path()
            })

        # ? Aloca os campos necessários de acordo com o modelo 
        serializer = serializers.UserSerializerPut(data =request.data)
        try:
            # ? Verifica a validade dos campos
            serializer.is_valid(raise_exception=True)
                
            
            # ? Realiza o update dos dados
            user = serializer.update(request.user,serializer.validated_data)

            # ? TODO: ADicionar no HIstorico do Usuário essas ALTERÇÔES
            models.HistoricUser.objects.create(user=request.user, suject=request.user,action="ATT",motive="atualização")

            return Response({"message":"Update Sucessful" , "data":{'name':user.name,"email":user.email,"city":user.city,"country":user.country}})
        except Exception as ex:

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
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)('background-task', {
            'type': 'send_message_discord', 
            'user': request.user.email,
            'action': request.method,
            'from':request.META.get('REMOTE_ADDR'),
            'url': request.get_full_path()
            })
        try:
            user = models.User.objects.get(pk = request.user.id)
            user.delete()
            return Response({"message":"Deleted Sucessful" })
        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


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



    


       
    