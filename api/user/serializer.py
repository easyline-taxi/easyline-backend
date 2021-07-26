from ..models import User,Point
from rest_framework import serializers
from django.utils import timezone
from easyline.utils import genAction,genEmployee

class UserSerializerRegister(serializers.HyperlinkedModelSerializer):
    confirm_password = serializers.CharField(max_length=100)
    name_of_point = serializers.CharField(max_length=200, required=False)

    class Meta:
        model = User
        fields = ['name', 'cpf', 'deviceid', 'email', 'city', 'country',
                  'password', 'confirm_password', 'name_of_point']
    #
    # Adaptação pra adicionar o usuário novo
    #

    def create(self, validated_data):
        #
        # remover pos não pertence ao modelo
        #
        confirm_password = validated_data.pop('confirm_password')
        name_of_point = validated_data.pop('name_of_point')
        user = None
        #
        # validação
        #
        if confirm_password != validated_data.get('password'):
            raise Exception('Senhas não são iguais')
        #
        # Cria o usuário depois vincular ao ponto
        #
        
        cpfValidado = User.cpfValidator(None, validated_data.get('cpf'))
        if cpfValidado:
            validated_data['cpf'] = cpfValidado
            user = User.objects.create_user(**validated_data,username=validated_data.get('email'))

        else:
            raise Exception('Invalid CPF')

        
        if name_of_point:
            
            #
            # Verifica validade desse usuário
            #

            if not user:
                raise Exception('User Inválido')

            #
            # Cria o ponto!
            #
            try:

                point = Point.objects.create(owner=user, name=name_of_point)

                #
                # adiciona os históricos iniciais
                #
                point.historic = []
                point.employee = []
                point.historic.append(genAction(user,"Entrou no Ponto","admin"))
                point.employee.append(genEmployee(user,"admin",point.name))
                
                # 
                # salvar os modelos
                # 

                point.save()
                user.save()
            except Exception as ex:
                user.delete()
                raise Exception(ex)
        # 
        # Retorna o user criado
        # 
        return user


class UserSerializerPut(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['vtr', 'name',"city",'country']



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['vtr', 'name',"city",'country']
