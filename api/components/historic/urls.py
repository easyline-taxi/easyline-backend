from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('user', views.HistoricUserViewSet,basename="HistoricUser")

urlpatterns = [ ] + router.urls