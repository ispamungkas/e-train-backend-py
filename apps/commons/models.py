from django.db import models

import time

from django.db import Error, models

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class BaseModel(models.Model):
    created_at = models.IntegerField(default=time.time)
    updated_at = models.IntegerField(null=True)
    
    def update(self):
        self.updated_at = time.time()
    
    class Meta:
        abstract = True
    
class SoftDelete(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.IntegerField(default=0)
    objects = SoftDeleteManager()
    all_objects = models.Manager()
    
    def restore(self):
        self.is_deleted = False
        self.save()
    
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = time.time()
        self.save()
    
    def delete(self):
        raise Error()
    
    class Meta:
        abstract = True
        