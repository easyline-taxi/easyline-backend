from django.shortcuts import render
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from .models import User
from rest_framework.response import Response
from .serializer import UserSerializer,UserSerializerRegister
from rest_framework.views import APIView

# Create your views here.

# @login_required(login_url='/login')
def homepage(request):
    return render(request,'index.html')


class UserDataView(APIView):
    serializer_class = UserSerializer

    def post(self, request, format=None):
        """
        Return data user
        """
        print(request.user)
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

class RegisterUsers(viewsets.ViewSet):

    permission_classes = []
    serializer_class = UserSerializerRegister

    def create(self, request):
        serializer = UserSerializerRegister(data =request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.create(validated_data = serializer.validated_data)
        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Nome": user.name,"Email":user.email})
       
    