from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        try:
            self.user = self.scope.get("user")
            if self.user != None:
                self.accept()
                self.send(text_data="[Welcome %s!]" % self.user.username)
            else:
                raise Exception("Usuário Inválido")
        except Exception as exe:
            self.close(message=exe)
            
    
        
    def receive(self, text_data=None,bytes_data=None ):
        if text_data.startswith("/name"):
            self.user.username = text_data[5:].strip()
            self.send(text_data="[set your username to %s]" % self.user.username)
        else:
            self.send(text_data=self.username + ": " + text_data)

    def close(self, status_code):
        self.send(status_code)
        return 