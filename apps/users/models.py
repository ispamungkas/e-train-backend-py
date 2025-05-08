import time

from django.db import models
from django.utils.timezone import now
from datetime import timedelta

def file_location(instance, filename, **kwargs):
    file_path = f'images/profile/{instance.nip}--{time.time()}-{filename}'
    return file_path

# Create your models here.
class User(models.Model):
    
    class RoleChoice(models.TextChoices):
        TEACHER = 'Teacher'
        HEADSCHOOL = 'Head School'
        SUPERUSER = 'Super User'
    
    name = models.CharField(max_length=30 )
    nip = models.CharField(max_length=20, unique=True)  
    password = models.CharField(max_length=10)
    email = models.EmailField(null= True, unique=True)
    address = models.TextField(null= True)
    p_number = models.CharField(max_length=14, null= True)
    gender = models.CharField(max_length=1, null=True)
    l_edu = models.CharField(max_length=20, null=True)
    c_school = models.CharField(max_length=20, null=True)
    dob = models.IntegerField(default = 0)
    role = models.CharField(max_length=20, choices=RoleChoice.choices, null=True)
    img_profile = models.ImageField(null= True, max_length=None, upload_to=file_location)
    created_at = models.IntegerField(default=time.time)
    updated_at = models.IntegerField(default=time.time)
    deleted_at = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_valid(self):
        return self.created_at >= now() - timedelta(minutes=5)
    
    