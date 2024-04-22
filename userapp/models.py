from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=64, unique=True)
    display_name = models.CharField(max_length=64)
    creation_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table="user"

