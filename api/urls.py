from django.urls import path, include
from rest_framework_jwt.views import refresh_jwt_token,verify_jwt_token
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('auth/refresh/',refresh_jwt_token, name='token_refresh'),
    path('auth/verify/', verify_jwt_token, name='token_verify'),
    path('auth/login/',views.ObtainJSONWebToken.as_view()),
    path('auth/register/',views.RegisterUsers.as_view()),
    path('user/',include('api.components.user.urls')),
    path('point/',include('api.components.point.urls')),
    path('plan/',include('api.components.plan.urls')),
    path('historic/',include('api.components.historic.urls')),
    path('admin/',include('api.components.admin.urls'))
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

