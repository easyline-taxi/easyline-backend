from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .serializer import PointRegisterSerializer
from django.utils.translation import gettext as _
from rest_framework.response import Response

# ! Imports do APP
from api.models import Point, PointEmployee, HistoricPoint, HistoricUser

# class PointGerals(viewsets.ViewSet):
#     serializer_class = None

#     def list(self, request):
#         # TODO: Listagem de Pontos
#         pass

#     def create(self, request):
#         # TODO: Criação de Ponto
#         pass

#     def retrieve(self, request, pk=None):
#         # TODO: informação dos pontos Ou Entrada no ponto
#         pass

#     def update(self, request, pk=None):
#         # TODO: Atualizar um ponto
#         pass


class PointRegister(APIView):
    serializer_class = PointRegisterSerializer

    def post(self, request, format=None):
        # TODO Criar um ponto vinculado ao usuário
        serializer = PointRegisterSerializer(data=request.data)

        try:
            # ? Verifica a validade dos dados
            serializer.is_valid(raise_exception=True)
            print(serializer.data)

            # ? Cria o ponto
            point = Point.objects.create(owner=request.user, name=serializer.data.get('name', None), city=serializer.data.get(
                'city', None), country=serializer.data.get('country', None), plan=serializer.data.get('plan', None))
            if point != None:
                HistoricPoint.objects.create(
                    point=point, suject=request.user, motive="Ponto fundado", action="fundacao")
                HistoricUser.objects.create(
                    user=request.user, suject=request.user, motive="Criou o ponto", action="fundacao")
                PointEmployee.objects.create(
                    user=request.user, point=point, function="admin")
            return Response({"message": _("Point Created"), "data": {'name': point.name, "city": point.city, "country": point.country}})
        except Exception as ex:
            return Response({"message": _(str(ex))}, status=status.HTTP_400_BAD_REQUEST)


class PointUserAction (APIView):
    # TODO: Ações user(comum)/point

    def get(self, request, format=None):
        # TODO: Pega os pontos relacionado ao user
        try:
            pontos_trabalhados = PointEmployee.objects.filter(user=request.user)
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
        # TODO: Deleitar qual ponto será ativado pelo usuário

        # ! Validation deviceid
        try:

            pontos_trabalhados = PointEmployee.objects.all().filter(user=request.user)
            ponto_selecionado = [
                x for x in pontos_trabalhados if x.point.id == request.data.get('point')]
            if ponto_selecionado != None:
                request.user.point_id = ponto_selecionado[0].point.id
                request.user.save()
                return Response({"message": "Point Selected "+str(request.user.point_id)})
        except Exception as ex:
            return Response({"message": "Point does not exists " + str(request.data.get('point'))}, status=status.HTTP_400_BAD_REQUEST)


class PointOwnerAction(APIView):
    def delete(self, request, format=None):
        # TODO: Deletar o ponto
        point = request.data.get('point')
        print(">>> ", point)
        if point == None:
            return Response({"message": "Point is invalid " + str(request.data.get('point'))}, status=status.HTTP_400_BAD_REQUEST)
        pontos_administrados = PointEmployee.objects.all().filter(
            user=request.user, function="admin")
        p = [x for x in pontos_administrados if x.point.id == point]
        if len(p) == 1:
            ponto = Point.objects.get(pk=p[0].point.id)
            ponto.delete()
            return Response({"message": "Point Deleted with Sucessful"})
        return Response({"message": "Point does not exists: " + str(request.data.get('point'))}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        # TODO: Transferir o ponto
        pass
