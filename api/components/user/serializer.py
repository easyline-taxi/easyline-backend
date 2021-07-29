from rest_framework import serializers
from django.utils import timezone
from easyline.utils import genAction,genEmployee

# ! Import from App
from api.models import User,Point,HistoricPoint,HistoricUser,PointEmployee


class UserSerializerRegister(serializers.HyperlinkedModelSerializer):
    # TODO: Adiciona o novo usuário padronizando o tal

    # ? Fields Adicionais ao modelo do user
    confirm_password = serializers.CharField(max_length=100)
    name_of_point = serializers.CharField(max_length=200, required=False)

    class Meta:
        model = User
        # ! name of point não vai
        fields = ['name', 'cpf', 'deviceid', 'email', 'city', 'country',
                  'password', 'confirm_password', 'name_of_point']
   

    def create(self, validated_data):
        # TODO: Processod e criação do usuário
        
        # ! Remoção das labels que não perdecem ao modelo
        confirm_password = validated_data.pop('confirm_password')
        name_of_point = validated_data.pop('name_of_point')
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
        
        # ? se tiver o nome do ponto, vamos criar o ponto junto
        if name_of_point:
            
            # ? Verifica se o usuário foi realmente criado
            if not user:
                raise Exception('User Inválido')

            # ? Inicio do processo de criação do ponto
            try:
                point = Point.objects.create(owner=user, name=name_of_point)
                
                # ? Adiciona os históricos
                HistoricPoint.objects.create(point = point,suject=user,motive="Criação do Ponto",action="fundacao")
                HistoricPoint.objects.create(point = point,suject=user,motive="Adicionado no Ponto",action="adicao")
                HistoricUser.objects.create(user = user,suject=user,motive="Adicionado no Ponto",action="adicao")
                PointEmployee.objects.create(user=user,function="admin")

                # 
                # salvar os modelos
                # 

                point.save()
                user.save()
            except Exception as ex:
                if point:
                    point.delete()
                if user:
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
