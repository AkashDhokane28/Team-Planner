from django.db import models
from teamapp.models import *
from django.utils import timezone

class Board(models.Model):
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    board_name = models.CharField(max_length=64,null=True, blank=True ,unique=True)
    board_description = models.TextField(max_length=128,null=True,blank=True)
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ("In PROGRESS", 'In Progress')
    )
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='OPEN')
    created_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)


class Task(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ("In PROGRESS", 'In Progress')
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    creation_time = models.DateTimeField(auto_now_add=True)