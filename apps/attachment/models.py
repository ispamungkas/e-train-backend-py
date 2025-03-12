import time

from django.db import models

from apps.commons.models import BaseModel, SoftDelete
from apps.users.models import User
from apps.enrolls.models import Enroll

def file_location_karya_nyata(instance, filename, **kwargs):
    file_path = f'file/karya_nyata/{time.time()}-{filename}'
    return file_path

def file_location_certificate(instance, filename, **kwargs):
    file_path = f'file/karya_nyata/{time.time()}-{filename}'
    return file_path

# Create your models here.
class KaryaNyata(BaseModel, SoftDelete):
    
    class KaryaNyataStatus(models.TextChoices):
        PENDING = 'pending', 'PENDING'
        DECLINE = 'decline', 'DECLINE',
        ACCEPTED = 'accepted', 'ACCEPTED'
    
    att = models.FileField(upload_to=file_location_karya_nyata)
    enroll = models.ForeignKey(Enroll, related_name='karyanyata', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='karyanyata', on_delete=models.CASCADE)
    status = models.CharField(choices=KaryaNyataStatus.choices, default=KaryaNyataStatus.PENDING, max_length=15)
    
    
class Certificate(BaseModel, SoftDelete):
    user = models.ForeignKey(User, related_name='certificate', on_delete=models.CASCADE)
    enroll = models.ForeignKey(Enroll, related_name='certificate', on_delete=models.CASCADE)
    cert = models.FileField()
    
class QRVerification(BaseModel, SoftDelete):
    code = models.CharField(max_length=100)