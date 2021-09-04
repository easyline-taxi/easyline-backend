from .applications.tasks.backgroundtask import BackgroundTaskConsumer

channels_urlspattern = {
            # Executa as background tasks
            "background-task": BackgroundTaskConsumer.as_asgi(),
        }

"""
To run:
# ! Runworker só escuta uma tarefa de cada vez então deve ser dividido em vários

python manage.py runworker background-task
"""