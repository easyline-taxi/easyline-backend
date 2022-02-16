from django.apps import AppConfig
class TaskConfig(AppConfig):
    name = 'api_async.components.task'

    def ready(self):
        try:
            from .applications.setup_task import setup
            setup()
        except Exception as ex:
            print("Necessita definir as tarefas nas função", ex)

        
    
    
