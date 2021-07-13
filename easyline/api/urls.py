from rest_framework import routers
from django.urls import path, include
from user.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet,basename='users')

urlpatterns = [
    path('api/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]