#  Function easy to call a bot discord

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
def sendMessage(message=None,request = None, user = None):
    channel_layer = get_channel_layer()

    if request:
        async_to_sync(channel_layer.send)('background-task', {
            'type': 'send_message_discord', 
            'user': request.user.email,
            'action': request.method,
            'from':request.META.get('REMOTE_ADDR'),
            'url': request.get_full_path(),
            'date': timezone.now().strftime("%m/%d/%Y, %H:%M:%S")
            })
    else:
        async_to_sync(channel_layer.send)('background-task', {
            'type': 'send_message_discord', 
            'message': message,
            'user': user.email,
            'date': timezone.now().strftime("%m/%d/%Y, %H:%M:%S")
            })
