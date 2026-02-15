from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    temperature = models.FloatField(default=25.0)