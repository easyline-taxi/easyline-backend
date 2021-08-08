from django.urls import path, include

from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('login/',views.ObtainJSONWebToken.as_view()),
    path('register/',views.RegisterUsers.as_view()),
    path('user/',include('api.components.user.urls')),
    path('point/',include('api.components.point.urls')),
    path('plan/',include('api.components.plan.urls'))
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

