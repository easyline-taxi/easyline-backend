
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from ..BaseTaskManager import BaseTaskManager
from django.utils import timezone
import logging
import requests
import json
from django.conf import settings

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
            
            send={
                "type": message.get('action', None),
                "title": message.get('user', None),
                "description": "{}\n{}".format(message.get('url', None),message.get('from', None)),
                "color": message.get('color', "#f3faff"),

            }
            try:
                requests.post("http://"+settings.URL_BOT_DISCORD+"/",json=send)
            except Exception as ex:
                pass

            

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