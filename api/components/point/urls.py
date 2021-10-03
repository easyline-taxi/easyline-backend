from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('historic',views.HistoricPointViewSet)


urlpatterns = [
    # ! TODO: Actions do ponto
    # ? Criar ponto
    path('register/', views.PointRegister.as_view()),
    
    # ? Pegar pontos 
    path('', views.PointUserAction.as_view()),

    # ? Deletar ponto
    # ? Transferir ponto
    path('config/', views.PointOwnerAction.as_view()),
    
    # ? adicionar user no ponto
    # ? Remover user do ponto
    path('actions/', views.PointOwnerUserAction.as_view()),


    # TODO: Actions da Fila

    # ? subir pessoa
    # ? descer pessoa
    # ? tripular
    # ? entrar na fila
] + router.urls
