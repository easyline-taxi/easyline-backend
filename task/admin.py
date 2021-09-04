from django.contrib import admin
from .models import Task, Completed_Task, Task_Until
# Register your models here.

# admin.site.register(Task)

# admin.site.register(Completed_Task)

# admin.site.register(Task_Until)

@admin.register(Task,Completed_Task,Task_Until)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status','created_at','expire_at','execute_until','error')
    

