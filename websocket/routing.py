from django.urls import path
from . import consumers

url_patterns = [
    path('ws/row/', consumers.Location.as_asgi())
]