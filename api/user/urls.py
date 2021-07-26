from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.UserDataView.as_view(), name='data'),
]
