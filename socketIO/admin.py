from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.ClientWebsocket)
class PointRowAdmin(admin.ModelAdmin):
    list_display = ['user','user_id','sid','created_at']

@admin.register(models.HistoricWebsocket)
class PointRowAdmin(admin.ModelAdmin):
    list_display = ['user','user_id','sid','action','created_at']
