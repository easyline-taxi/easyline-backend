from django.contrib import admin
from api import models


# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Plan)
admin.site.register(models.PointEmployee)
admin.site.register(models.PointRow)
admin.site.register(models.HistoricPoint)
admin.site.register(models.HistoricUser)
admin.site.register(models.DeviceId)

class TokenAdmin(admin.ModelAdmin):
    list_display = ['user','is_valid','last_login','key']
class PointAdmin(admin.ModelAdmin):
    list_display = ['id','name','owner']
admin.site.register(models.Point,PointAdmin)

admin.site.register(models.Token,TokenAdmin)
