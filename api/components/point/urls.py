from django.urls import path, include
from . import views



urlpatterns = [
    # ! TODO: Actions do ponto
    # ? Criar ponto
    path('register/', views.PointRegister.as_view()),
    
    # ? Pegar pontos 
    path('', views.PointUserAction.as_view()),


    # TODO: Actions da Fila

    # ? subir pessoa
    # ? descer pessoa
    # ? tripular
    # ? entrar na fila
] 
