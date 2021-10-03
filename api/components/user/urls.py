from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('historic', views.HistoricUserViewSet,basename="HistoricUser")

urlpatterns = [
    # ? Mostrar os dados do usuário GET
    # ? Atualizar os dados PUT
    # ? deletar os usuários DELETE
    path('', views.UserDataView.as_view(), name='data')
] + router.urls
