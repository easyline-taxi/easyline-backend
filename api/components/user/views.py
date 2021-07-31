from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializer import UserSerializerPut,UserSerializer
from rest_framework.views import APIView
import base64
import io
from PIL import Image
# ! Import From App
from api.models import User,Point,PointEmployee

class UserDataView(APIView):
    serializer_class= UserSerializer

    def get(self, request, format=None):
        #  TODO: Retorna os dados do usuário

        # ? Verifica se o deviceId é correspondente ao usuário
        # ! não tem necessidade
        # if not str(request.user.deviceid) == str(request.data.get('deviceid')):
        #     return Response({"message": "DeviceId Invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        # ? Procura os pontos trabalhados
        pontos_trabalhados = PointEmployee.objects.all().filter(user=request.user)
# request.META.get('HTTP_HOST')+
        # _file = open(, 'rb')
        b64iamge = None
        try:

            # ? get image
            image = Image.open(request.user.photo)
            
            # ?get image size
            (width, height) = image.size 
            if width > 70 or height > 70:

                # ? Resize Image
                image = image.resize((70,70), Image.ANTIALIAS)
                image.save(request.user.photo.path)

            # ?Convert do base64
            output = io.BytesIO()
            image.save(output, format=image.format)
            b64 = base64.b64encode(output.getvalue()).decode('utf-8')
            b64iamge = "data:image/"+image.format+";base64,"+b64
        except Exception as ex:
            pass
        
        return Response({
            "user_data":
                {
                    "id":request.user.id,
                    "vtr":request.user.vtr,
                    "name":request.user.name,
                    "email":request.user.email,
                    "photo":b64iamge
                },
            "point_data": [
                {
                    "id":x.point.id,
                    "name":x.point.name,
                    "owner_id": x.point.owner.id,
                    "onlines":PointEmployee.objects.all().filter(point=x.point).count(),
                    "function": x.function
                } for x in pontos_trabalhados]})

    def put(self,request, format=None):
        # TODO: Atualiza os dados do usuário
        
        # ? Verifica se o deviceId é correspondente ao usuário
        if not str(request.user.deviceid) == str(request.data.get('deviceid')):
            return Response({"message": "DeviceId Invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        # ? Aloca os campos necessários de acordo com o modelo 
        serializer = UserSerializerPut(data =request.data)
        try:
            # ? Verifica a validade dos campos
            if not serializer.is_valid(raise_exception=True):
                return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
            
            # ? Realiza o update dos dados
            user = serializer.update(request.user,serializer.validated_data)

            return Response({"message":"Update Sucessful" , "data":{'name':user.name,"email":user.email,"city":user.city,"country":user.country}})
        except Exception as ex:

            # ? Senão retorna erro 404
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,format=None):
        # TODO: Deleta o usuário
        try:
            request.user.delete()
            return Response({"message":"Deleted Sucessful" })
        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


       
    