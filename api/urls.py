from django.urls import path, include

from api.views import RegisterUsers
from rest_framework import routers

router = routers.DefaultRouter()




urlpatterns = [
    path('register/',RegisterUsers.as_view()),
    path('user/',include('api.user.urls')),
    path('api/point/',include('api.point.urls')),
    path('api/plan/',include('api.plan.urls'))
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

