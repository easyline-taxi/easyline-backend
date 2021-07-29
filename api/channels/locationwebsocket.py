

from channels.generic.websocket import WebsocketConsumer
# Aqui será dedicado a pegar as posições do usuário em relação ao ponto e colocar na fila

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        try:
            self.user = self.scope["user"]
            if self.user != None:
                self.accept()
                self.send(text_data="[Welcome %s!]" % self.user.username)
            else:
                raise Exception("Usuário Inválido")
        except Exception as exe:
            self.close(message=exe)
            # self.disconnect()
    
            

    def receive(self, text_data=None,bytes_data=None ):
        if text_data.startswith("/name"):
            self.user.username = text_data[5:].strip()
            self.send(text_data="[set your username to %s]" % self.user.username)
        else:
            self.send(text_data=self.username + ": " + text_data)

    def disconnect(self, message):
        self.send(message)
        pass