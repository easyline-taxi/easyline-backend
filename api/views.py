from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.utils import timezone


# ! Acessos do App
from api.models import User,Point,HistoricPoint,HistoricUser,PointEmployee,DeviceId

from django.contrib.auth import authenticate
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from django.utils.translation import ugettext as _
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
class UserSerializerRegister(serializers.HyperlinkedModelSerializer):
    # ?: Adiciona o novo usuário padronizando o tal

    # ? Fields Adicionais ao modelo do user
    confirm_password = serializers.CharField(max_length=100)
    deviceid = serializers.CharField(max_length=150)
    class Meta:
        model = User
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
            raise Exception('Senhas não são iguais')
        
        # ? Validação do CPF
        cpfValidado = User.cpfValidator(None, validated_data.get('cpf'))
        if cpfValidado:
            validated_data['cpf'] = cpfValidado
            user = User.objects.create_user(**validated_data,username=validated_data.get('email'))
            # vincula device id ao usuário
            if len(DeviceId.objects.filter(deviceid=deviceid)):
                # ! Possivelmente usuário está logando no celular de outro usuário (Como tratar?)
                user.delete()
                raise Exception("deviceId já vinculado a um usuário")
            DeviceId.objects.create(deviceid=deviceid, user=user)
        else:
            raise Exception('Invalid CPF')
        
        # 
        # Retorna o user criado
        # 
        return user

# TODO fazer um desvinculador de device ID só pra admin

class RegisterUsers(APIView):

    permission_classes = []
    serializer_class = UserSerializerRegister

    def post(self, request):
        serializer = UserSerializerRegister(data =request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.create(validated_data = serializer.validated_data)
            return Response({"Nome": user.name,"Email":user.email})
        except Exception as ex:
                
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
                    msg = _('DeviceId is required.')
                    raise serializers.ValidationError(msg)
                devices = DeviceId.objects.filter(user=user,deviceid=attrs.get("deviceid"))
                if not len(devices):
                    # ! Usuário logou em aparelho diferente
                    DeviceId.objects.create(user=user,deviceid=attrs.get("deviceid"))
                else:
                    devices[0].last_used = timezone.now()
                    devices[0].save()

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
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
    serializer_class = JSONWebTokenSerializer