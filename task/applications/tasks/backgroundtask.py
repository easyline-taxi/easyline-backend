
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from task.models import Task,Task_Until
from ..BaseTaskManager import BaseTaskManager
from django.db.models import Q
from time import sleep
from django.utils import timezone
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)



class BackgroundTaskConsumer(BaseTaskManager):
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