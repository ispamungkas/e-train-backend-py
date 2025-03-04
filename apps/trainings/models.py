import time

from django.db import models

class Status(models.TextChoices):
    UNCOMPLETED = 'Uncompleted'
    COMPLETED = 'Completed'

# Create your models here.
class Training(models.Model):
    class TypeTrain(models.TextChoices):
        ONLINE = 'Online'
        OFFLINE = 'Offline'
    
    name = models.CharField(max_length=20)
    desc = models.TextField()
    type_train = models.CharField(max_length=10, choices=TypeTrain.choices)
    img = models.ImageField(max_length=None)
    location = models.TextField(null=True)
    link = models.URLField(max_length=200)
    date = models.IntegerField()
    total_jp = models.PositiveIntegerField()
    is_open = models.BooleanField()
    created_at = models.IntegerField(default=time.time)
    deleted_at = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
class Section(models.Model):
        
    name = models.CharField(max_length=10)
    status = models.CharField(max_length=15,choices=Status.choices, default=Status.UNCOMPLETED)
    jp = models.PositiveIntegerField()
    train_id = models.ForeignKey(Training, on_delete=models.CASCADE)
    created_at = models.IntegerField(default=time.time)
    deleted_at = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
class Topic(models.Model):
    
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.UNCOMPLETED)
    content = models.TextField()
    created_at = models.IntegerField(default=time.time)
    deleted_at = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name