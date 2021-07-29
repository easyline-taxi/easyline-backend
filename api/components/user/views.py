from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializer import UserSerializerPut,UserSerializer
from rest_framework.views import APIView

# ! Import From App
from api.models import User,Point

class UserDataView(APIView):
    serializer_class= UserSerializer
    def post(self, request, format=None):
        """
        Return data user
        """
     
        if not str(request.user.deviceid) == str(request.data.get('deviceid')):
            return Response({"message": "DeviceId Invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        pontos_trabalhados = [x for x in Point.objects.all() for y in x.employee if y.get('cpf') == request.user.cpf and y.get('deviceid') == request.user.deviceid]

        return Response({
            "user_data":
                {
                    "id":request.user.id,
                    "vtr":request.user.vtr,
                    "name":request.user.name,
                    "email":request.user.email
                },
            "point_data": [
                {
                    "id":x.id,
                    "name":x.name,
                    "owner_id": x.owner.id,
                    "employees":len(x.employee)
                } for x in pontos_trabalhados]})

    def put(self,request, format=None):
        """
            Atualizar os dados
        """
        
        if not str(request.user.deviceid) == str(request.data.get('deviceid')):
            return Response({"message": "DeviceId Invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializerPut(data =request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = serializer.update(request.user,serializer.validated_data)
            # return user
            return Response({"message":"Update Sucessful" , "data":{'name':user.name,"email":user.email,"city":user.city,"country":user.country}})
        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)



       
    