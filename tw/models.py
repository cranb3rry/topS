from django.db import models

# Create your models here.

class TwitchStat(models.Model):
    subs = models.PositiveSmallIntegerField()
    views = models.IntegerField()
    status = models.BooleanField()