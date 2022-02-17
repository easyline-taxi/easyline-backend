from rest_framework.views import APIView
from api import models
from django.forms.models import model_to_dict
from asgiref.sync import async_to_sync
from rest_framework import exceptions
from channels.layers import get_channel_layer
class APIView(APIView):
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'view': self,
        }
        
    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


def list_onlines(point):
    return models.PointEmployee.objects.filter(point=point).count()
        
def list_points(point_employee):
    # monta dict de respostas
    y = model_to_dict(point_employee.point)
    # y.update({"id": point_employee.point.id})
    y.update({"function": point_employee.function})
    y.update({"onlines": list_onlines(point_employee.point)})
    return y

def sendLogDiscord(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)('background-task', {
        'type': 'send_message_discord', 
        'user': request.user.email,
        'action': request.method,
        'body':request.data,
        'from':request.META.get('REMOTE_ADDR'),
        'url': request.get_full_path()
        })

def pontosTrabalhados(user,point_id = -2):
    """trazer os pontos e filtragem de permissão de pontos

    Args:
        user ([type]): usuário da requisição
        point_id ([type], optional): Id do ponto para filtragem. Defaults to None.

    Raises:
        exceptions.NotAcceptable: Usuário (id: {}) não possui deviceId Registrado
        exceptions.NotAcceptable: Usuário (id: {}) não possui um ponto válido.

    Returns:
        [type]: [description]
    """
    device = models.DeviceId.objects.filter(user=user).order_by('-last_used').first()
    if not device:
        raise exceptions.NotAcceptable("Usuário (id: {}) não possui deviceId Registrado.".format(user.id))
    
    # ? Procura os pontos trabalhados
    pontos_trabalhados = models.PointEmployee.objects.filter(deviceid=device,deviceid__user=user)
    if point_id is None:
        raise exceptions.NotAcceptable("PointId registrado pelo user (id:{}) é None.".format(user.id))
    if point_id == -1:
        raise exceptions.NotAcceptable("PointId solicitado pelo user (id:{}) é Inválido".format(user.id))
    if point_id >= 0:
        ponto_atual = pontos_trabalhados.filter(point__id=point_id).first()
        if not ponto_atual:
            raise exceptions.NotAcceptable("Usuário (id: {}) não pertence a esse ponto.".format(user.id))
        return ponto_atual
    return pontos_trabalhados
     
    