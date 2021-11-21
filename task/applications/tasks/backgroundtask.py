
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from ..BaseTaskManager import BaseTaskManager
from django.utils import timezone
import logging
import requests
import json

channel_layer = get_channel_layer()
logger = logging.getLogger(__name__)

# send_event_to_point imports
from consumer import models as consumer_models


class BackgroundTaskConsumer(BaseTaskManager):
    
    
    def send_event_to_point(self,message,*args, **kwargs):
        """Envia as mensagens parametradas para todos os clientes relacionados a um determinado ponto (Via Websocket)

        Args:
            point (int): Fala qual ponto ocorreu o evento
            event_type: Qual evento que está sendo transmitido
        """
        nametask = message.get('type',__name__)
        
        def callback(message,*args, **kwargs):
            point = message.get('point',None)
            event_type = message.get('event_type',None)
            
            if not point or not event_type:
                raise Exception("Ponto ou Evento Não identificado!")
            
            clients = consumer_models.Client.objects.filter(user__point_id=point)
            for client in clients:
                async_to_sync(channel_layer.send)(client.channel, {
                    "type": "send.event",
                    "content": json.dumps({"event":event_type, "send_at": timezone.now().strftime('%d-%m-%y %H:%M:%S')}),
                })
            
        self.orquestrador(message,callback,nametask=nametask, *args, **kwargs)
    
    def send_message_discord(self, message, *args, **kwargs):
        """
            Tasks agendadas no database
        """
        nametask = message.get('type',__name__)


        def callback(message,*args, **kwargs):
            # DEFINE A FUNÇÃO DA TAREFA AQUI
            # raise NotImplementedError()
            
            payload = {
                "content": "===========================\naction: {}\nuser: {}\nurl: {}\nfrom: {}\ndate: {}\ntime: {}\n===========================\n".format(message.get('action', None),message.get('user', None),message.get('url', None),message.get('from', None),timezone.now().date(),timezone.now().time()),
                "tts": "true"
            }

            
            if payload.get("content"):
                header = {
                "authorization": "Bot ODE4NDc2MjIxMjgwODEzMDg2.YEYnYQ.IRGH9F0DU4iIWOT7r9DdwZhzJnk"
                }

                r = requests.post("https://discord.com/api/v9/channels/818475844770070529/messages", data=payload,headers=header)

            

            #####################
            # Content da tarefa #
            #####################
            pass
        
        self.orquestrador(message,callback,nametask=nametask, *args, **kwargs)

    
    


"""


def callback_example(self, message, *args, **kwargs):
        nametask = __name__

        def callback():
            # DEFINE A FUNÇÃO DA TAREFA AQUI
            # 

            #####################
            # Content da tarefa #
            #####################
            raise NotImplementedError()

            ############################
            # Fim do Content da tarefa #
            ############################

        self.orquestrador(message,callback,nametask=nametask, *args, **kwargs)

"""