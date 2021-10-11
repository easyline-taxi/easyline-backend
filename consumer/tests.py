from django.test import TestCase
from channels.testing import WebsocketCommunicator
from .consumers import MessageConsumer

class TestsConsumerlvl1(TestCase):
    async def test_my_consumer(self):
        communicator = WebsocketCommunicator(MessageConsumer, "/consumer/")
        connected, subprotocol = await communicator.get_response()
        assert connected
        await communicator.send_to(text_data="Meu teste")
        response = await communicator.receive_from()
        assert response == "hello"
        await communicator.disconnect()