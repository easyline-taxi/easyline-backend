


from rest_framework import status
from .models import User
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
from api.components.user.serializer import UserSerializerRegister

class RegisterUsers(APIView):

    permission_classes = []
    serializer_class = UserSerializerRegister

    def post(self, request):
        serializer = UserSerializerRegister(data =request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.create(validated_data = serializer.validated_data)
            return Response({"Nome": user.name,"Email":user.email})
        except Exception as ex:
                
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)