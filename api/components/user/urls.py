from django.urls import path, include
from . import views
from api import routers

router = routers.CustomNoLookUpRouter()
# router.register("new",views.UserDataViewset,'user')


urlpatterns = [
    # ? Mostrar os dados do usuário GET
    # ? Atualizar os dados PUT
    # ? deletar os usuários DELETE
    path('', views.UserDataView.as_view(), name='data')

]+router.urls
