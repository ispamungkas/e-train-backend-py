import time

from django.db import models

from apps.commons.models import BaseModel, SoftDelete
from apps.users.models import User
from apps.trainings.models import Training

def file_location_karya_nyata(instance, filename, **kwargs):
    file_path = f'file/karya_nyata/{time.time()}-{filename}'
    return file_path

def file_location_certificate(instance, filename, **kwargs):
    file_path = f'file/certificate/{time.time()}-{filename}'
    return file_path

class Enroll(BaseModel, SoftDelete):
    
    class Enroll_Status(models.TextChoices):
        NEEDACTION = 'need action', 'NEED ACTION'
        PROGRESS = 'progress', 'PROGRESS'
        TIMEOUT = 'time out', 'TIME OUT'
        COMPLETED = 'completed', 'COMPLETED'
    
    train = models.ForeignKey(Training, related_name='enrolls', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='enrolls', on_delete=models.CASCADE)
    status = models.CharField(choices=Enroll_Status.choices, default=Enroll_Status.NEEDACTION, max_length=20)
    p_learn = models.PositiveIntegerField(default=0)
    s_learn = models.PositiveIntegerField(default=0)
    attandence = models.BooleanField(default=False)
 
    
