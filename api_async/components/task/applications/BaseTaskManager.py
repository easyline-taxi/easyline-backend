import logging
from django.utils import timezone
from django.db.models import Q
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from time import sleep
from channels.consumer import SyncConsumer
from ..models import Task,Task_Until, Completed_Task
import uuid
import json
import threading
from datetime import datetime
logger = logging.getLogger(__name__)
# logger.basicConfig(format='(Background Task) :%(message)s',)





class BaseTaskManager(SyncConsumer):



    def finalize_task(self,task: Task, error=None):
        if error:
            task.error = True
            logger.info("Task %s Encerrado com error!" % task.name)

        else:
            logger.info(" Task %s completada!" % task.name)

        data = {
            "name": task.name,
            "status": not task.status,
            "expire_at": task.expire_at,
            "error_message": error
        }

        Completed_Task.objects.create(**data)
        task.delete()
    
        
    def orquestrador(self, message, callback, nametask, *args, **kwargs):
        """
            Função destinada a padronizar o sistema de execução de tarefas, mostrando os modelos 
        """

        host = message.get("host", '127.0.0.1')
      

        data = {
            "name": str(nametask),
            "status": True,
            "repeat": message.get("repeat", 0),
            "expire_at": message.get('expire_at', None),
            "execute_until": message.get("execute_until", None),
            "parameters": {"message":message,"args": args, "kwargs":kwargs,"nametask":nametask}
        }

        task = None
        # Registra a tarefa
        try:
            if data.get("execute_until"):
                data['execute_until'] = datetime.strptime(data['execute_until'],'%d/%m/%y %H:%M:%S')
                task = Task_Until.objects.create(**data)
            elif not len(Task.objects.filter(name=nametask)):
                task = Task.objects.create(**data)
            else:
                print("Ja existe essa task em execução")
                return

        except Exception as ex:
            logger.error("(Background Task) >> Dados Inválidos", ex)
            return 

        logger.info("Iniciando a task " + task.name)
        # Resolved TODO: Falta Executar consulta de forma agendada (na data ocorrer o evento ) (vai ser un checagem de tempo em tempo)
        
        #############################
        # Tarefas Orientadas a DATA #
        #############################
        

        if task.execute_until:
            if timezone.now() >= task.execute_until:
                self.finalize_task(task, error="Tarefa Expirada")
            return

            # Caso esteja ok, então ela é colocada na fila para ser executada em outro processo

        # else:
        #     # Se não possui tempo, então ela é imediata
        #     callback()
        #     self.finalize_task(task)
        #     return 

        ##################################
        # Tarefas Orientadas a REPETIÇÃO #
        ##################################

        

        # Torne infinita, passível a ser finalizada

        threading.Thread(target=self.task_thread, args=(task,callback,message)).start()

    def execute_task_until(self, message, *args, **kwargs):
        #  ! Funcionalidade Importante
        """
            Executa as tasks agendadas no database
        """
        nametask = message.get('type',__name__)

        def callback(host= 'localhost'):
            # DEFINE A FUNÇÃO DA TAREFA AQUI

            #####################
            # Content da tarefa #
            #####################
            # channel_layer = get_channel_layer()

            # async_to_sync(channel_layer.group_send)(
            #     host,
            #     {
            #         "type": "public.message",
            #         "text": "task agendada %s - %s" % (nametask, host),
            #     },
            # )

            tasks = Task_Until.objects.all().order_by('-execute_until')

            try:
                if len(tasks) > 0:
                    task = tasks[0]

                    # Checa a por data
                    # if task.get('execute_until').date() >  timezone.now().date():
                    #     # Espera até 5 min antes de executar
                    #     # sleep((timezone.now()-task.execute_until).total_seconds() - timezone.timedelta(minutes=task.execute_until_interval).total_seconds())
                    #     pass
                    if timezone.now().date() >task.execute_until.date():
                        # Cancelar o alerta por erro
                        self.finalize_task(task, error="Passou do tempo limite")
                        return 
                    
                    # se for igual ao dia:
                    # if task.get('execute_until').time() > timezone.now().time():
                    #     # Espera até 5 min antes de executar
                    #     sleep((timezone.now()-task.get('execute_until')).total_seconds() - timezone.timedelta(minutes=task.get('execute_until_interval')).total_seconds())
                    if task.execute_until.time() < timezone.now().time():
                        # Cancelar o alerta por erro
                        self.finalize_task(task, error="Passou do tempo limite")
                        return 

                    # se a data for maior q agora e menos que agora + algum tempo, então é executável
                    if task.execute_until >= timezone.now() and task.execute_until <= task.execute_until+timezone.timedelta(minutes=task.execute_until_interval):
                        # ! aqui roda a função callback(host)
                        channel_layer = get_channel_layer()
                        params = task.parameters.get('message')

                        # Replica as passagens
                        async_to_sync(channel_layer.send)('background-task', 
                        {'type': params.get('type'),
                        'host':params.get('host')})
                        self.finalize_task(task)
                        return
                    # se a data for maior q agora e maior que agora + algum tempo, então é passível a espera
                    elif task.execute_until >= timezone.now() and task.execute_until + timezone.timedelta(minutes=task.execute_until_interval) > timezone.now():
                        return 
                    else:
                        # Cancelar o alerta por erro
                        self.finalize_task(task, error="Passou do tempo limite")
                        return 
                            
            except Exception as ex:
                self.finalize_task(task, error=ex)
                return 



            ############################
            # Fim do Content da tarefa #
            ############################

        self.orquestrador(message,callback,nametask=nametask, *args, **kwargs)


    def task_thread(self, task: Task, callback,message=None):


        # ? se não for repetitível então executar apenas uma vez
        if not task.repeat:
            try:
                callback(message)
                self.finalize_task(task)
                return

            except Exception as ex:
                self.finalize_task(task, error=ex)
                logger.error(ex)
                return 
        try:
            while task.repeat:
                # atualiza a task
                task = Task.objects.get(pk=task.pk)

                if task.complete:
                    self.finalize_task(task)
                    return

                if task.expire_at:
                    # caso possa expirar
                    if timezone.now() >= task.expire_at:
                        self.finalize_task(task)
                        return

                if not task.status:
                    # Fica dormindo quanto não está sendo usada
                    task = Task.objects.get(pk=task.pk)
                    sleep(60)
                    continue
                callback(message)
                sleep(task.repeat)
            # Caso esteja desativada, deve ser terminada
            self.finalize_task(task)
            return
        except Exception as ex:
            self.finalize_task(task, error=ex)
            logger.error(ex)
            return
