from django.db import models
from userapp.models import *

class Team(models.Model):
    users = models.ManyToManyField(User)
    team_name = models.CharField(max_length=64, null=True, blank=True, unique=True)
    team_description=models.TextField(max_length=128,null=True,blank=True)
    created_timestamp=models.DateTimeField(auto_now_add=True)

