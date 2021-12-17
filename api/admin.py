from django.contrib import admin
from api import models


# Register your models here.

admin.site.register(models.Plan)
@admin.register(models.PointRow)
class PointRowAdmin(admin.ModelAdmin):
    list_display = ['position','user_id','user','point_id']
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email','last_login','point_id']
    
@admin.register(models.PointEmployee)
class PointEmployeeAdmin(admin.ModelAdmin):
    list_display = ['id','point','point_id','deviceid','function']

@admin.register(models.HistoricPoint)
class HistoricPointAdmin(admin.ModelAdmin):
    list_display = ['id','action','suject','point_id','motive']
    
@admin.register(models.HistoricUser)
class HistoricUserAdmin(admin.ModelAdmin):
    list_display = ['id','action','suject','user','motive']
    
# admin.site.register(models.DeviceId)
@admin.register(models.DeviceId)
class DeviceIdAdmin(admin.ModelAdmin):
    list_display = ['user_id','deviceid','last_used','create_at']
    ordering = ['-last_used']
@admin.register(models.Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['user','is_valid','last_login','key']
@admin.register(models.Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ['id','name','owner']

