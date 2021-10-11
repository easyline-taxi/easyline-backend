from channels.generic.websocket import JsonWebsocketConsumer
from ..models import Client
import json
from django.utils import timezone
# from .models import 
from .actions.action import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime

channel_layer = get_channel_layer()

class MessageConsumerTest(JsonWebsocketConsumer):
    """
    Classe destinada a testes com websocket
    
    """

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
            async_to_sync(self.channel_layer.group_add)(str(self.scope.get('host','localhost')), self.channel_name)
            self.accept()

            
            # async_to_sync(channel_layer.send)('background-task', {
            # 'type': 'sendemail_task_until',
            # 'host':self.scope.get('host'),
            # 'execute_until':(timezone.now()+timezone.timedelta(minutes=1)).strftime('%d/%m/%y %H:%M:%S')})
            
            async_to_sync(channel_layer.send)('background-task', {
                'type': 'send_push_task_until',
                # Get host (Pegar do tenant)
                'host':self.scope.get('host'),
                # User para qual será enviado
                'user_id':user.id,
                # Content (O que chegará no frontend)
                'content': {
                    # Type a ser reconhecido pelo frontend
                    "type": "PUSH_MESSAGE",
                    # Nome da instituição, (Pegar do tentant)
                    "title": f"{client_tenant.objects.filter(domain_url=self.scope.get('host'))[0].tenant_name}",
                    # Mensagem
                    "message": "Atendimento",
                    # Texto Extenso
                    "bigText": "Seu atendimento foi agendado com sucesso",
                    # Texto Resumido
                    "subText": "O seu atendimento ocorrerá nos horários talz e tais"
                 },
                #  Quando será enviado
                'execute_until':(timezone.now()+timezone.timedelta(minutes=1)).strftime('%d/%m/%y %H:%M:%S')
            })

    
    def disconnect(self, close_code):
        user = self.scope.get('user', None)

        if user.is_anonymous:

            # saida do canal do usuário não autenticado
            print("Usuário Não Autenticado saiu")
        else:

            # Remove o usuário autenticado do canal público
            async_to_sync(self.channel_layer.group_discard)(str(self.scope.get('host','localhost')), self.channel_name)
            Client.objects.filter(channel=self.channel_name).delete()
            print(self.scope.get('user').email+" Saiu")
       
    def receive(self,text_data):
        try:
            data = json.loads(text_data)
            data['action'] = actions_exists(action=data.get("action",None))
            if data.get('action'):
                self.send_json({"response": "o campo 'action' é necessario"})
                return
        except Exception as ex:
            self.send_json({"err": "Formatacao do JSON invalida"})
            return
        
        print(self.channel_name)
        response = actions_list(data['action'])
        print(response)
        
        self.send_json(response)

    def public_message(self, event):
        # Envia para o grupo

        # Poderia ser usado sistema de notificação em realtime


        # Handles the "chat.message" event when it's sent to us.
        print("Send to group")
        print(event)
        self.send_json(event["text"])

        # async_to_sync(self.channel_layer.group_send)(
        #     "public",
        #     {
        #         "type": "public.message",
        #         "text": data,
        #     },
        # )
    