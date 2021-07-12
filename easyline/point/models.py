from djongo import models
from django import forms
from user.models import User
from plan.models import Plan

# Create your models here.

class Point(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    local = models.JSONField(default='{}')
    name = models.CharField(max_length=200)
    employees = models.JSONField(default='{}')
    historic = models.JSONField(default='{}')
