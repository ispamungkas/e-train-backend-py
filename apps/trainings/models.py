import time

from django.db import models
from apps.commons.models import BaseModel, SoftDelete

class Status(models.TextChoices):
    UNCOMPLETED = 'uncompleted','Uncompleted'
    COMPLETED = 'completed', 'Completed'

def file_location(instance, filename, **kwargs):
    file_path = f'images/training/{time.time()}-{filename}'
    return file_path

def file_location_content(instance, filename, **kwargs):
    file_path = f'images/content/{instance.name}--{time.time()}-{filename}'
    return file_path

# Create your models here.
class Training(BaseModel, SoftDelete):
    class TypeTrain(models.TextChoices):
        WEBINAR = 'webinar', 'Webinar'
        TRAINING = 'training', 'Training'
        
    class TypeTrainAc(models.TextChoices):
        ONLINE = 'online', 'Online'
        OFFLINE = 'offline', 'Offline'
    
    name = models.CharField(max_length=20)
    desc = models.TextField()
    type_train = models.CharField(max_length=10, choices=TypeTrain.choices, default=TypeTrain.TRAINING)
    type_train_ac = models.CharField(max_length=10, choices=TypeTrainAc.choices, default=TypeTrainAc.ONLINE)
    attend = models.IntegerField()
    img = models.ImageField(max_length=None, upload_to=file_location)
    location = models.TextField(null=True)
    link = models.URLField(max_length=200, null=True)
    dateline = models.IntegerField(default=time.time)
    is_publish = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    
class Section(BaseModel, SoftDelete):
        
    name = models.CharField(max_length=10)
    status = models.CharField(max_length=15,choices=Status.choices, default=Status.UNCOMPLETED)
    jp = models.PositiveIntegerField(default=0)
    train_id = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='sections')
    
    def __str__(self):
        return self.name
    
class Topic(BaseModel, SoftDelete):
    
    section_id = models.ForeignKey(Section, related_name='topics', on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    img = models.ImageField(upload_to=file_location_content, max_length=None, null=True)
    content = models.TextField(null=True)
    
    def __str__(self):
        return self.name