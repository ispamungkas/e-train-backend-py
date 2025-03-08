import time

from django.db import models

from apps.commons.models import BaseModel, SoftDelete
from apps.users.models import User
from apps.trainings.models import Training

def file_location_karya_nyata(instance, filename, **kwargs):
    file_path = f'file/karya_nyata/{time.time()}-{filename}'
    return file_path

def file_location_certificate(instance, filename, **kwargs):
    file_path = f'file/karya_nyata/{time.time()}-{filename}'
    return file_path

class Enroll(BaseModel, SoftDelete):
    
    class Enroll_Status(models.TextChoices):
        NEEDACTION = 'need action', 'NEED ACTION'
        PROGRESS = 'progress', 'PROGRESS'
        TIMEOUT = 'time out', 'TIME OUT'
        COMPLETED = 'completed', 'COMPLETED'
    
    train_id = models.ForeignKey(Training, related_name='enrolls', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, related_name='enrolls', on_delete=models.CASCADE)
    status = models.CharField(choices=Enroll_Status.choices, default=Enroll_Status.NEEDACTION, max_length=20)
    out_date = models.IntegerField()
    p_learn = models.PositiveIntegerField(default=0)
    S_learn = models.PositiveIntegerField(default=0)
    
    def __init__(self, *args, **kwargs):
        return self.name
    
