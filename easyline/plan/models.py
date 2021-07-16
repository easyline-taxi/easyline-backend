from djongo import models

from django.utils import timezone

# Create your models here.

class Plan(models.Model):
    name = models.CharField(max_length=200)
    value  = models.IntegerField()
    on_created = models.DateField(default=timezone.now())
    permissions = models.JSONField(default={"permissions": []})