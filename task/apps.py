from django.apps import AppConfig
class TaskConfig(AppConfig):
    name = 'task'

    def ready(self):
        try:
            from task.applications.setup_task import setup
            setup()
        except Exception as ex:
            print("Necessita definir as tarefas nas função", ex)

        
    
    
