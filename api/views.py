from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers


# ! Acessos do App
from api.models import User,Point,HistoricPoint,HistoricUser,PointEmployee

class UserSerializerRegister(serializers.HyperlinkedModelSerializer):
    # TODO: Adiciona o novo usuário padronizando o tal

    # ? Fields Adicionais ao modelo do user
    confirm_password = serializers.CharField(max_length=100)

    class Meta:
        model = User
        # ! name of point não vai
        fields = ['name', 'cpf', 'deviceid', 'email', 'city', 'country',
                  'password', 'confirm_password']
   

    def create(self, validated_data):
        # TODO: Processod e criação do usuário
        
        # ! Remoção das labels que não perdecem ao modelo
        confirm_password = validated_data.pop('confirm_password')
        user = None
        
        # ? Validação da SENHA
        if confirm_password != validated_data.get('password'):
            raise Exception('Senhas não são iguais')
        
        # ? Validação do CPF
        cpfValidado = User.cpfValidator(None, validated_data.get('cpf'))
        if cpfValidado:
            validated_data['cpf'] = cpfValidado
            user = User.objects.create_user(**validated_data,username=validated_data.get('email'))
        else:
            raise Exception('Invalid CPF')
        
        # 
        # Retorna o user criado
        # 
        return user


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