from django.shortcuts import render

# Create your views here.
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# # ENVIO DE LOG DO BOT DISCORD
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.send)('background-task', {
#             'type': 'send_message_discord', 
#             'user': request.user.email,
#             'action': request.method,
#             'from':request.META.get('REMOTE_ADDR'),
#             'url': request.get_full_path()
#             })