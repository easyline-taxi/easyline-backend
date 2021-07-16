from rest_framework import routers
from django.urls import path, include

from user.views import RegisterUsers
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'register', RegisterUsers, basename='User')


urlpatterns = [
    path('', include(router.urls)),
    path('api/user/',include('user.urls')),
    path('api/point/',include('point.urls')),
    path('api/plan/',include('plan.urls'))
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

