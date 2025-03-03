import time
from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30)
    nip = models.CharField(max_length=20)
    password = models.CharField(max_length=10)
    email = models.EmailField(null= True)
    address = models.TextField(null= True)
    p_number = models.CharField(max_length=14, null= True)
    gender = models.CharField(max_length=1, null=True)
    l_edu = models.CharField(max_length=20, null=True)
    c_school = models.CharField(max_length=20, null=True)
    role = models.CharField(max_length=20, null=True)
    created_at = models.IntegerField(default=time.time)
    deleted_at = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name