from django.apps import AppConfig
class ConsumerConfig(AppConfig):
    name = 'api_async.components.consumer'

    def ready(self):
        # resolved TODO: Remover todas as conexões websocket
        try:
            # para resolver o problema do primeiro tenant que não existe ao migrar a primeira vez
            from .models import Client as clientSock
            try:
                clientSock.objects.all().delete()
            except Exception as ex:
                print(ex)
        except Exception as ex:
            pass
        

        
