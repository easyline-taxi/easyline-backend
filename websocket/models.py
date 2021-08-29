from django.db import models
from django.utils import timezone
# Create your models here.

from api.models import User

class Client(models.Model):
    # Client Websocket
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.CharField(max_length=200)
    created_at = models.DateTimeField( default=timezone.now)

    def __str__(self):
        return str(self.channel)
