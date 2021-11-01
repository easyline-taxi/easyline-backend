from channels.generic.websocket import JsonWebsocketConsumer
from ..models import Client
import json
from django.utils import timezone
# from .models import
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime
from . import utils
from .actions import action
from rest_framework import exceptions
from task import utils as utils_bot_discord
channel_layer = get_channel_layer()

"""
Example json comunicate

{
    "action":"SET_LOCALE",
    "params": {
        "coordinate":
            {
                
            }
        }
}


"""


class MessageConsumer(JsonWebsocketConsumer):

    def connect(self):
        user = self.scope.get('user', None)

        if user.is_anonymous:
            # Se não estiver logado, vai ser desconectado
            self.close(code=404)
        else:

            #  Se tiver login vai logar e entrar no canal público
            print(user.email+" Entrou >>")

            # Salva o canal do usuário vinculado ao user
            Client.objects.create(user=user, channel=self.channel_name)

            async_to_sync(self.channel_layer.group_add)(
                'public', self.channel_name)

            utils_bot_discord.sendMessage(message="websocket (connected)",user=user)
            self.accept()

    def disconnect(self, close_code):
        user = self.scope.get('user', None)
        utils_bot_discord.sendMessage(message="websocket (disconected) >> "+str(close_code),user=user)
        if user.is_anonymous:

            # saida do canal do usuário não autenticado
            print("Usuário Não Autenticado saiu")
        else:

            # Remove o usuário autenticado do canal público
            async_to_sync(self.channel_layer.group_discard)(
                'public', self.channel_name)
            Client.objects.filter(channel=self.channel_name).delete()
            print(self.scope.get('user').email+" Saiu")

    def receive(self, text_data):
        #  Se houver erros nas requisições, o usuário sai da FILA
        try:
            user = self.scope.get('user', None)
            response = {"detail": "Nothing"}

            data = json.loads(text_data)
          
            # Distribui funções que são requisitadas pela aplicação
            utils.check_action(data)
        
            if action.actions_exists(action=data.get('action')):
                response = getattr(action, data.get("action"))(user, data.get("params"))
                response['action'] = data.get("action")
            self.send_json(response)

        except Exception as ex:
            print(str(ex))
            self.close(str(ex))

    def public_message(self, event):
        # Envia para o grupo
        # Handles the "public.message" event when it's sent to us.
        self.send_json(event["text"])

        # async_to_sync(self.channel_layer.group_send)(
        #     'public',
        #     {
        #         "type": "public.message",
        #         "text": data,
        #     },
        # )
