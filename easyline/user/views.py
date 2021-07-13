from django.shortcuts import render
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets

from .models import User
from rest_framework.response import Response
from .serializer import UserSerializer
from rest_framework.views import APIView

from rest_framework_simplejwt import authentication
# Create your views here.

# @login_required(login_url='/login')
def homepage(request):
    return render(request,'index.html')


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)

    serializer_class = UserSerializer
    queryset = User.objects.all()
       
    