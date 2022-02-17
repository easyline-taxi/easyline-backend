from django.db import connection
import logging
from django.utils import timezone
from django.db.models import Q
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from time import sleep
from ..models import Task, Completed_Task
import uuid
import json
from django.conf import settings
logger = logging.getLogger(__name__)

def setup():
    """
        Adicionar as tarefas disponíveis no database e executar ao iniciar o servidor
    """

    channel_layer = get_channel_layer()
    # Inicia todas as tarefas de forma pausada
    try:
        logger.debug("Iniciando as tarefas de background compartilhadas")

        # Remove todas as tarefas pendentes que não possuem prazo
        Task.objects.filter(execute_until=None).delete()

        # Executa todas as tasks com o campo 'execute until'
        async_to_sync(channel_layer.send)('background-task', {
            'type': 'execute_task_until',
            'repeat':15, 
            'host':'127.0.0.1'
            })

        # TASKS dos arquivo de Task
        # async_to_sync(channel_layer.send)('background-task', {
        #     'type': 'send_message_discord', 

        #     })

            # ! O que essa task faz exatamente?
        # async_to_sync(channel_layer.send)('background-task', {
        #     'type': 'notify_user',
        #     'host':tenant.domain_url,
        #     'repeat':10, 
        #     })
        
        # Tem objetivo de rodar qualquer task que necessite de um looping infinito
        # ! Exemplo importante
        # async_to_sync(channel_layer.send)('background-task', {
        #     'type': 'task_looping',
        #     'host':tenant.domain_url,
        #     'repeat':15, 
        #     })

    except Exception as e:
        logger.error(e)