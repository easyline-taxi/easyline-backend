from django.contrib import admin
from api.models import User,Plan,Point,PointEmployee, HistoricPoint, HistoricUser, PointRow, DeviceId


# Register your models here.

admin.site.register(User)
admin.site.register(Plan)
admin.site.register(Point)
admin.site.register(PointEmployee)
admin.site.register(PointRow)
admin.site.register(HistoricPoint)
admin.site.register(HistoricUser)
admin.site.register(DeviceId)