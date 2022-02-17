from django.contrib import admin
from .models import Client

# Register your models here.

@admin.register(Client)
class PointRowAdmin(admin.ModelAdmin):
    list_display = ['user','user_id','channel','created_at']