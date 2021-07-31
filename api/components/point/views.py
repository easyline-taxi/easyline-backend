from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .serializer import PointRegisterSerializer

# ! Imports do APP
from api.models import Point

# class PointGerals(viewsets.ViewSet):
#     serializer_class = None

#     def list(self, request):
#         # TODO: Listagem de Pontos
#         pass

#     def create(self, request):
#         # TODO: Criação de Ponto
#         pass

#     def retrieve(self, request, pk=None):
#         # TODO: informação dos pontos Ou Entrada no ponto
#         pass

#     def update(self, request, pk=None):
#         # TODO: Atualizar um ponto
#         pass



class PointRegister(APIView):
    serializer_class= PointRegisterSerializer

    def post(self,request):
        # TODO Criar um ponto vinculado ao usuário

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
        
        pass
