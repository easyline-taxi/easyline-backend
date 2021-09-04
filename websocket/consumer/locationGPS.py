from channels.generic.websocket import WebsocketConsumer
from ..models import Client
import json
from django.utils import timezone
# from .models import 
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync,sync_to_async


channel_layer = get_channel_layer()

class Location(WebsocketConsumer):

    def connect(self):
        user = self.scope.get('user', None)      


        if user.is_anonymous:
            # Se não estiver logado, vai ser desconectado
            self.close(code=404)
        else: 

            #  Se tiver login vai logar e entrar no canal público
            print(user.email+" Entrou >>")

            # cria canal públic
            Client.objects.create(user= user, channel=self.channel_name)
            async_to_sync(self.channel_layer.group_add)("public", self.channel_name)
            self.accept()

            


            # async_to_sync(channel_layer.send)('background-task', {'type': 'task_notify_user','host':self.scope.get('host'),'repeat':5})

    
    def disconnect(self, close_code):
        user = self.scope.get('user', None)
        

        if user.is_anonymous:

            # saida do canal do usuário não autenticado
            print("Usuário Não Autenticado saiu")
        else:

            # Remove o usuário autenticado do canal público
            async_to_sync(self.channel_layer.group_discard)("public", self.channel_name)
            Client.objects.filter(channel=self.channel_name).delete()
            print(self.scope.get('user').email+" Saiu")
       
    def receive(self,text_data):
        data = text_data
        try:
            data= json.loads(text_data)
          
        except Exception as ex:
            self.send({"err": "Formatacao do JSON invalida"})
            
        print(data)
        
        print(self.channel_name)


    def public_message(self, event):
        # Envia para o grupo

        # Poderia ser usado sistema de notificação em realtime


        # Handles the "chat.message" event when it's sent to us.
        print("Send to group")
        print(event)
        self.send(event["text"])

        # async_to_sync(self.channel_layer.group_send)(
        #     "public",
        #     {
        #         "type": "public.message",
        #         "text": data,
        #     },
        # )
    