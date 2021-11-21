from django.urls import path
from . import views


urlpatterns = [
    # ? Deletar ponto
    # ? Transferir ponto
    path('config/', views.PointOwnerAction.as_view()),
    # ? adicionar user no ponto
    # ? Remover user do ponto
    path('actions/', views.PointOwnerUserAction.as_view()),
    # ? Transferencias de cargos
    path('transfer/', views.ChangeUserFunctionViewSet.as_view()),
    path('getHistoric/',views.HistoricPOintViewSet.as_view())
] 
