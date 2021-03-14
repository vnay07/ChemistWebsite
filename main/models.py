from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Buisness(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(serialize=False,auto_created=True, max_length=100)
    ordered_date = models.DateTimeField(default=timezone.now)
    
    def __str__ (self):
    
        return self.name
    