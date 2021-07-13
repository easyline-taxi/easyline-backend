from djongo import models
from django.contrib.auth.models import AbstractUser
import bson
import re
# Create your models here.

# converter cpf para string sem pontuação
cpfConverter = lambda cpf: ''.join(re.findall("\d", cpf))

class User(AbstractUser, models.Model):
    cpf = models.CharField(max_length=20)
    vtr = models.IntegerField(default=None, blank=True)
    name=models.CharField(max_length=300)

    # validar cpf
    def cpfValidator(self,cpf:str):
        cpf = cpfConverter(cpf)
        if len(cpf)!=11:
            return False
        if cpf=='00000000000' or cpf=='11111111111' or cpf=='22222222222' or cpf=='33333333333' or cpf=='44444444444' or cpf=='55555555555' or cpf=='66666666666' or cpf=='77777777777' or cpf=='88888888888' or cpf=='99999999999':
            return False
        return True

    def __str__(self):
        return self.email
