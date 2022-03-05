from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
from django.forms import CharField

from django.utils import timezone
# Create your models here.

User = get_user_model()
class ClientWebsocket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    sid = models.CharField(max_length=200,default= uuid4())
    point = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default=timezone.now)

class HistoricWebsocket(models.Model):
    action = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complement = models.TextField(null=True)
    sid = models.CharField(max_length=200)
    point = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default=timezone.now)