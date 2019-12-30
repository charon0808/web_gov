

# Create your models here.
from django.db import models


class Running(models.Model):
    dataset = models.CharField(max_length=160)
    algorithm = models.CharField(max_length=320)
    status = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

