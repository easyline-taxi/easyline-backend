from channels.generic.websocket import WebsocketConsumer


# class MyConsumer(WebsocketConsumer):
#     groups = ["broadcast"]

#     def connect(self):
#         # Called on connection.
#         # To accept the connection call:
#         self.accept()
#         # Or accept the connection and specify a chosen subprotocol.
#         # A list of subprotocols specified by the connecting client
#         # will be available in self.scope['subprotocols']
#         self.accept("subprotocol")
#         # To reject the connection, call:
#         self.close()

#     def receive(self, text_data=None, bytes_data=None):
#         # Called with either text_data or bytes_data for each frame
#         # You can call:
#         self.send(text_data="Hello world!")
#         # Or, to send a binary frame:
#         self.send(bytes_data="Hello world!")
#         # Want to force-close the connection? Call:
#         self.close()
#         # Or add a custom WebSocket error code!
#         self.close(code=4123)

#     def disconnect(self, close_code):
#         # Called when the socket closes

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
            print(exe)
            self.send(text_data="User not authenticated")
            # self.disconnect()
    
            

    def receive(self, *, text_data):
        if text_data.startswith("/name"):
            self.username = text_data[5:].strip()
            self.send(text_data="[set your username to %s]" % self.username)
        else:
            self.send(text_data=self.username + ": " + text_data)

    def disconnect(self, message):
        pass