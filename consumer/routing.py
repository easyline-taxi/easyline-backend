from django.urls import re_path, path
from . import consumers

urlpatterns = [
    path('ws/row/', consumers.MessageConsumer.as_asgi()),
    # path('ws/test/', consumers.MessageConsumerTest.as_asgi()),
]
