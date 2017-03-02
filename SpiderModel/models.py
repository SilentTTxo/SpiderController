from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    username = models.TextField()
    password = models.TextField()
    power = models.IntegerField()

class Spider(models.Model):
    name = models.TextField()
    uid = models.IntegerField()
    other = models.TextField()
    param = models.TextField()
