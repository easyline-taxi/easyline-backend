from django.contrib.auth.models import AbstractUser

from djongo import models 

# from django.db import models
from django.utils import timezone
import re
# Create your models here.

# converter cpf para string sem pontuação
cpfConverter = lambda cpf: ''.join(re.findall("\d", cpf))

def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     print(instance)
#     print(filename)
#     return 'images/user_{0}'.format(filename)
    return 'user_{0}/{1}'.format(instance.user.id, filename)
class User(AbstractUser,models.Model):
    # ?: Dados armazenados dos usuários

    # ? Itens obrigatórios
    email= models.EmailField(max_length=254, unique=True)
    cpf = models.CharField(max_length=11, unique=True,default="00000000000")

    # ? Itens não obrigatórios
    vtr = models.IntegerField(default=None, blank=True)
    name = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=100, blank= True, null=True)
    country = models.CharField(max_length=100, blank= True, null=True)
    photo = models.ImageField(upload_to='images/',null=True)
    active = models.BooleanField( default=True)

    # ? Ponto sendo trabalhado

    point_id=models.IntegerField(null=True)

    def is_active(self):
        return self.active

    # ? Validação do CPF
    def cpfValidator(self,cpf:str):
        cpf = cpfConverter(cpf)
        if len(cpf)!=11:
            return False
        if cpf=='00000000000' or cpf=='11111111111' or cpf=='22222222222' or cpf=='33333333333' or cpf=='44444444444' or cpf=='55555555555' or cpf=='66666666666' or cpf=='77777777777' or cpf=='88888888888' or cpf=='99999999999':
            return False
        return cpf

    def __str__(self):
        return self.email

class DeviceId(models.Model):
    deviceid= models.CharField(max_length=150, default="00000000000")
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    last_used = models.DateTimeField(default=timezone.now)
    create_at = models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return str(self.deviceid)

class Plan(models.Model):
    # ? Adição de Planos Futuros
    name = models.CharField(default="Free", max_length=200)
    value  = models.IntegerField(default = 0)
    on_created = models.DateField(default=timezone.now)
    permissions = models.JSONField(default={})

class Point(models.Model):
    # ? descrição do modelo de dados dos Pontos de Taxi

    # ? Dono do ponto
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # ? Plano Atual, se for Null é o Free
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)

    # ? Dados do ponto
    local = models.JSONField(default={})
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=50,null=True,blank=True)
    country = models.CharField(max_length=100, blank= True, null=True)

    def __str__(self):
        return self.name

class Historic(models.Model):
    # ?: Histórico padronizado do usuário para armazenamento de ações

    ACTIONS_HISTORIC ={
        ("T","transferido"),
        ("F","fundado"),
        ("P","penalizado"),
        ("EP","entrou no ponto"),
        ("MB","movido para baixo"),
        ("MC","movido para cima"),
        ("ATT","atualizado"),
        ("REM","removido"),
        ("ADD","adicionado"),
        ("TRI","tripulado"),

    }

    # ? Ação realizada ex: ban, expulso, embarcado
    action = models.CharField(max_length=5, choices=ACTIONS_HISTORIC, default="ADD")

     # ? Motivo da ação
    motive = models.CharField(max_length=300)

    # ? usuário que foi afetado
    suject = models.ForeignKey(User, on_delete=models.SET_DEFAULT , default=None, null=True)

     # ? Data em que ocorreu
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.motive

class HistoricPoint(Historic):
    # ?: Dados referente ao historico do Point
    # ? ponto em que foi realizado
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
class HistoricUser(Historic):
    # ?: Dados referente ao historico do User
    # ? usuário que foi realizado uma função
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT , default=None, null=True)

class PointRow(models.Model):
    # ? Descrição das filas

    # ? ponto referente
    point = models.ForeignKey(Point, on_delete=models.PROTECT)
    
    # ? ID Usuário na Fila 
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    
    # ? Posição em que se encontrava, se null é pq saiu da Fila
    position = models.IntegerField()
    date = models.DateTimeField(default = timezone.now)

    # ? Se o ping websocket está ativo
    online = models.BooleanField(default=False)


    def __str__(self):
        return str(self.position)+" "+str(self.user_id)

class PointEmployee(models.Model):
    CARGOS_POINT ={
        ("M","motorista"),
        ("A","admin"),
        ("P","prancheteiro")
    }

    # ?: Listar os usuários que fazem parte de um ponto
    point = models.ForeignKey(Point, on_delete=models.CASCADE)

    # ? Vincula o device Id no ponto
    deviceid=models.ForeignKey(DeviceId, on_delete=models.CASCADE)

    # ? Função - Admin e motorista
    function = models.CharField(max_length=1,choices=CARGOS_POINT,default="M")

    # ? Caso o dono do ponto queira desligar do sistema
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.point.name)+" - "+self.function
