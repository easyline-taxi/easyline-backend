from djongo import models
from django.contrib.auth.models import AbstractUser
import re
# Create your models here.

# converter cpf para string sem pontuação
cpfConverter = lambda cpf: ''.join(re.findall("\d", cpf))

class User(AbstractUser, models.Model):
    email= models.EmailField(max_length=254, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    vtr = models.IntegerField(default=None, blank=True)
    name = models.CharField(max_length=300)
    city = models.CharField(max_length=100, blank= True, null=True)
    country = models.CharField(max_length=100, blank= True, null=True)
    admin = models.BooleanField(blank= True, null=True, default=False)
    deviceid= models.CharField(max_length=150,unique=True)

    # validar cpf
    def cpfValidator(self,cpf:str):
        cpf = cpfConverter(cpf)
        if len(cpf)!=11:
            return False
        if cpf=='00000000000' or cpf=='11111111111' or cpf=='22222222222' or cpf=='33333333333' or cpf=='44444444444' or cpf=='55555555555' or cpf=='66666666666' or cpf=='77777777777' or cpf=='88888888888' or cpf=='99999999999':
            return False
        return cpf

    def __str__(self):
        return self.email
