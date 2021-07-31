from django.urls import path, include
from . import views

urlpatterns = [
    # TODO: Actions do ponto
    # ? Criar ponto
    path('register/', views.PointRegister),
    
    # ? Pegar pontos
    # ? Deletar ponto
    # ? Transferir ponto
    # ? adicionar user no ponto
    # ? Remover user do ponto


    # TODO: Actions da Fila

    # ? subir pessoa
    # ? descer pessoa
    # ? tripular
    # ? entrar na fila
]
