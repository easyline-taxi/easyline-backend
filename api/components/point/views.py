from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .serializer import PointRegisterSerializer
from django.utils.translation import gettext as _
from rest_framework.response import Response

# ! Imports do APP
from api.models import Point,User, PointEmployee, HistoricPoint, HistoricUser,DeviceId

# class PointGerals(viewsets.ViewSet):
#     serializer_class = None

#     def list(self, request):
#         # ?: Listagem de Pontos
#         pass

#     def create(self, request):
#         # ?: Criação de Ponto
#         pass

#     def retrieve(self, request, pk=None):
#         # ?: informação dos pontos Ou Entrada no ponto
#         pass

#     def update(self, request, pk=None):
#         # ?: Atualizar um ponto
#         pass


class PointRegister(APIView):
    """
        Cria um ponto
    """
    # ? TODO: Setup Tests
    serializer_class = PointRegisterSerializer

    def post(self, request, format=None):
        # ? Criar um ponto vinculado ao usuário
        serializer = PointRegisterSerializer(data=request.data)

        try:
            # ? Verifica a validade dos dados
            serializer.is_valid(raise_exception=True)

            # ? Cria o ponto
            point = Point.objects.create(owner=request.user, name=serializer.data.get('name', None), city=serializer.data.get(
                'city', None), country=serializer.data.get('country', None), plan=serializer.data.get('plan', None))
            if point != None:
                HistoricPoint.objects.create(
                    point=point, suject=request.user, motive="Ponto fundado", action="F")
                HistoricUser.objects.create(
                    user=request.user, suject=request.user, motive="Criou o ponto", action="F")
                # ! find points by device id
                devices = DeviceId.objects.filter(user=request.user).order_by('-last_used')
                PointEmployee.objects.create(deviceid=devices[0], point=point, function="A")
            return Response({"message": _("Point Created"), "data": {'name': point.name, "city": point.city, "country": point.country}})
        except Exception as ex:
            return Response({"message": _(str(ex))}, status=status.HTTP_400_BAD_REQUEST)


class PointUserAction (APIView):
    # TODO: Setup Tests
    # ? Ações user(comum)/point

    def get(self, request, format=None):
        # ? Pega os pontos relacionado ao user
        try:
            # ! find points by device id
            devices = DeviceId.objects.filter(user=request.user).order_by('-last_used')
            pontos_trabalhados = PointEmployee.objects.filter(deviceid=devices[0])
            return Response({"message": "Pontos Encontrados", "points": [
                {
                    "id": x.point.id,
                    "name": x.point.name,
                    "owner_id": x.point.owner.id,
                    "onlines": PointEmployee.objects.filter(point=x.point).count(),
                    "function": x.function
                } for x in pontos_trabalhados]})
        except Exception as ex:
            return Response({"message": _(str(ex))}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        # ? Escolher qual ponto será trabalhado e ativado pelo usuário
        try:
            devices = DeviceId.objects.filter(user=request.user).order_by('-last_used')
            # ? Procura os pontos trabalhados
            pontos_trabalhados = PointEmployee.objects.all().filter(deviceid=devices[0])
            ponto_selecionado = [
                x for x in pontos_trabalhados if str(x.point.id) == str(request.data.get('point'))]
            if ponto_selecionado != None:
                request.user.point_id = ponto_selecionado[0].point.id
                request.user.save()
                return Response({"message": "Point Selected "+str(request.user.point_id)})
        except Exception as ex:
            return Response({"message": "Point does not exists " + str(request.data.get('point'))}, status=status.HTTP_400_BAD_REQUEST)


class PointOwnerAction(APIView):
    # TODO: Setup Tests

    def delete(self, request, format=None):
        # ?  Deletar o ponto
        point = request.data.get('point')
        if point == None:
            return Response({"message": "Point is invalid " + str(request.data.get('point'))}, status=status.HTTP_400_BAD_REQUEST)
        
        devices = DeviceId.objects.filter(user=request.user).order_by('-last_used')
        pontos_administrados = PointEmployee.objects.all().filter(
            deviceid=devices[0], function="A")
        p = [x for x in pontos_administrados if x.point.id == point]
        if len(p) == 1:
            ponto = Point.objects.get(pk=p[0].point.id)
            ponto.delete()
            return Response({"message": "Point Deleted with Sucessful"})
        return Response({"message": "Point does not exists: " + str(request.data.get('point'))}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        # ?: Transferir o ponto

        # ? get actual point 
        point = Point.objects.get(pk=request.user.point_id)
        
        # ? verifica se o usuário é dono do ponto atual
        if point.owner.id != request.user.id:
            return Response({"message": "Você não é dono do ponto"},status=status.HTTP_403_FORBIDDEN)

        # ? pega o email do usuário que ele quer transferir
        user = User.objects.get(email=request.data.get('email'))
        devices = DeviceId.objects.filter(user=user).order_by('-last_used')
        target = devices[0]

        #  ?: Verificar se o cara que ele quer transferir está no ponto
        if not len(PointEmployee.objects.filter(point=point,deviceid=target)):
            return Response({"message": "Usuário não pertence a este ponto"},status=status.HTTP_400_BAD_REQUEST)

        # ? Trasnfere a posse
        point.owner = target.user
        point.save()

        # ? trocar as posições
        
        device = DeviceId.objects.filter(user=request.user).order_by('-last_used')[0]
        employee = PointEmployee.objects.filter(point=point,deviceid=device)[0]
        employee.function = "M"
        employee.save()
        employee = PointEmployee.objects.filter(point=point,deviceid=target)[0]
        employee.function = "A"
        employee.save()

        # ? adicionar no histórico do ponto e do usuário

        HistoricPoint.objects.create(point=point, suject=request.user, motive="Transferência de Posse", action="T")
        HistoricUser.objects.create(user=request.user, suject=target.user, motive="Transferência de Posse", action="T")

        return Response({"message": "Ponto Transferido"})

class PointOwnerUserAction(APIView):
    # TODO: Setup Tests
    def post(self, request, format=None):
        # ? TODO: Adicionar usuários do ponto

        #  ? checa se o usuário TEM PERMISSAO para adicionar no point
        point = Point.objects.get(pk = request.user.point_id)
        if point.owner != request.user:
            return Response({"message": "Você não é dono do ponto"},status=status.HTTP_403_FORBIDDEN)
        
        # TODO: ADicionar as limitações do ponto com base nos planos

        # TODO Verificar se o usuário já esta cadastrado 

        # ? TODO: buscar pelo device id
        # ! deviceID (QRCODE) - como USER
        try:
            device = DeviceId.objects.filter(deviceid=request.data.get("deviceid")).order_by('-last_used')[0]
        except Exception as ex:
            return Response({"message": "DeviceId inválido"},status=status.HTTP_400_BAD_REQUEST)
        
        # ? TODO: Adicionar nos EMPLOYEEs
        PointEmployee.objects.create(deviceid=device, point=point, function="M")

        # ? TODO: Adicionar no histórico
        HistoricPoint.objects.create(point=point, suject=request.user, motive="Adicionou usuário", action="ADD")
        HistoricUser.objects.create(user=request.user, suject=device.user, motive="Adicionou usuário", action="ADD")

        return Response({"message": "Usuário Adicionado"})

    def delete(self,request,format=None):
        # TODO: Setup Tests
        """ TODO: Remover usuários do ponto """
        motive = "Removeu o usuário usuário"
        # ? TODO Verficiar o usuário tem permissão
        point = Point.objects.get(pk = request.user.point_id)
        if point.owner != request.user:
            return Response({"message": "Você não é dono do ponto"},status=status.HTTP_403_FORBIDDEN)
        
        # ! manda o email do cara
        device = DeviceId.objects.filter(deviceid=request.data.get("email")).order_by('-last_used')[0]
        if request.data.get("motive"):
            motive= request.data.get("motive")

        # ? TODO Verficiar se o usuário está no ponto
        
        if not len(PointEmployee.objects.filter(point=point,deviceid=device)):
            return Response({"message": "Usuário não pertence a este ponto"},status=status.HTTP_400_BAD_REQUEST)
        
        # ? TODO Remover o usuário
        employee = PointEmployee.objects.filter(point=point,deviceid=device)[0]
        employee.delete()
        
        # ? TODO Adicionar nos históricos
        HistoricPoint.objects.create(point=point, suject=request.user, motive=motive, action="REM")
        HistoricUser.objects.create(user=request.user, suject=device.user, motive=motive, action="REM")

        return Response({"message": "Usuário Removido"})
