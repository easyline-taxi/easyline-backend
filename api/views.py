from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers,exceptions
from django.utils import timezone
import os
import sys
# ! Acessos do App
from api import models

from django.contrib.auth import authenticate
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from django.utils.translation import ugettext as _
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import AllowAny

import logging
logger = logging.getLogger(__name__)

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
class UserSerializerRegister(serializers.HyperlinkedModelSerializer):
    # ?: Adiciona o novo usuário padronizando o tal

    # ? Fields Adicionais ao modelo do user
    confirm_password = serializers.CharField(max_length=100)
    deviceid = serializers.CharField(max_length=150)
    class Meta:
        model = models.User
        # ! name of point não vai
        fields = ['name', 'cpf', 'deviceid', 'email', 'city', 'country',
                  'password', 'confirm_password']
   

    def create(self, validated_data):
        # ?: Processod e criação do usuário
        
        # ! Remoção das labels que não perdecem ao modelo
        confirm_password = validated_data.pop('confirm_password')
        deviceid = validated_data.pop('deviceid')
        user = None
        
        # ? Validação da SENHA
        if confirm_password != validated_data.get('password'):
            raise exceptions.ValidationError('Senhas não são iguais')
        
        # ? Validação do CPF
        cpfValidado = models.User.cpfValidator(None, validated_data.get('cpf'))
        if cpfValidado:
            validated_data['cpf'] = cpfValidado
            validated_data['username'] = validated_data.get('email')
            print(type(validated_data), validated_data)
            
            user = models.User.objects.create_user(**validated_data)
            
            # vincula device id ao usuário
            logger.warning(user)
            # if len(models.DeviceId.objects.filter(deviceid=deviceid)):
            #     # ! Possivelmente usuário está logando no celular de outro usuário (Como tratar?)
            #     user.delete()
            #     raise Exception("deviceId já vinculado a um usuário")
            models.DeviceId.objects.create(deviceid=deviceid, user=user)
        else:
            raise Exception('Invalid CPF')
        
        # 
        # Retorna o user criado
        # 
        
        return user

# TODO fazer um desvinculador de device ID só pra admin

class RegisterUsers(APIView):

    permission_classes = [AllowAny]
    authentication_classes=[]
    serializer_class = UserSerializerRegister

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'view': self,
        }
        
    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
    

    def post(self, request):
        """
        Registro do usuário

        --
        """

        serializer = UserSerializerRegister(data =request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(validated_data = serializer.data)
        try:
            # Cria o token
            models.Token.objects.create(user=user)
            return Response({"Nome": user.name,"Email":user.email})
        except Exception as ex:
            logger.info(ex)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class JSONWebTokenSerializer(JSONWebTokenSerializer):
    deviceid = serializers.CharField(max_length=150)


    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }
        
        if all(credentials.values()):
            user = authenticate(**credentials)
            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
                if not attrs.get("deviceid"):
                    msg = _('DeviceId is required muito required.')
                    raise serializers.ValidationError(msg)
                devices = models.DeviceId.objects.filter(user=user,deviceid=attrs.get("deviceid"))
                if not len(devices):
                    # ! Usuário logou em aparelho diferente
                    models.DeviceId.objects.create(user=user,deviceid=attrs.get("deviceid"))
                else:
                    devices[0].last_used = timezone.now()
                    devices[0].save()

                payload = jwt_payload_handler(user)
                json_token = jwt_encode_handler(payload)
                token = models.Token.objects.filter(user=user)
                if token:
                    token[0].key = json_token
                    token[0].last_login = timezone.now()
                    token[0].save()
                    
                else:
                    models.Token.objects.create(user=user, key=json_token, last_login=timezone.now())

                return {
                    'token': json_token,
                    'user': user
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)
            
class ObtainJSONWebToken(ObtainJSONWebToken):
    permission_classes = [AllowAny]
    authentication_classes=[]
    serializer_class = JSONWebTokenSerializer