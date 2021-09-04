from django.db import models

from django.utils.translation import ugettext as _
from django.utils import timezone
import uuid
# Create your models here.

class Task(models.Model):
    uuid = models.UUIDField(_(""), default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(_(""), default=timezone.now)
    repeat = models.IntegerField(_("Repeate"), default=0)
    parameters = models.JSONField(_("Parametros"), blank=True, null=True)
    expire_at = models.DateTimeField(_(""), default=None, null=True, blank=True)
    execute_until = models.DateTimeField(_("Quando ela irá executar"), default=None, null=True, blank=True)
    execute_until_interval = models.IntegerField(_("Intervalo de atraso da task"),default=5)
    error = models.BooleanField(_("Falhou?"),default=False)
    complete=models.BooleanField(_("Para completar a task"), default=False)

    def __str__(self):
        return self.name+" - "+ str(self.uuid)

class Task_Until(models.Model):
    uuid = models.UUIDField(_(""), default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(_(""), default=timezone.now)
    repeat = models.IntegerField(_("Repeate"), default=0)
    parameters = models.JSONField(_("Parametros"), blank=True, null=True)
    expire_at = models.DateTimeField(_(""), default=None, null=True, blank=True)
    execute_until = models.DateTimeField(_("Quando ela irá executar"), default=None, null=True, blank=True)
    execute_until_interval = models.IntegerField(_("Intervalo de atraso da task"),default=5)
    error = models.BooleanField(_("Falhou?"),default=False)
    complete=models.BooleanField(_("Para completar a task"), default=False)

    def __str__(self):
        return self.name+" - "+ str(self.uuid)

class Completed_Task(models.Model):
    uuid = models.UUIDField(_(""), default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    parameters = models.JSONField(_("Parametros"), blank=True, null=True)
    error_message = models.TextField(_("Mensagem de erro"), blank=True, null=True)
    created_at = models.DateField(_(""), default=timezone.now)
    expire_at = models.DateTimeField(_(""), default=None, null=True, blank=True)
    execute_until = models.DateTimeField(_(""), default=None, null=True, blank=True)
    error = models.BooleanField(default=False)
    finalize_at = models.DateTimeField(_(""), default=timezone.now)
    
    def __str__(self):
        return self.name+" - "+ str(self.uuid)
