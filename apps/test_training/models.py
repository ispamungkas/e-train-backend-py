import json

from django.db import models

from apps.commons.models import BaseModel, SoftDelete
from apps.trainings.models import Training, Section
from apps.users.models import User

class PostTest(BaseModel, SoftDelete):
    train = models.ForeignKey(Training, related_name='post_tests', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, related_name='post_tests', on_delete=models.CASCADE)
    question = models.JSONField(null=True, default=dict)

class Answer(BaseModel, SoftDelete):
    post = models.ForeignKey(PostTest, related_name='answers', on_delete=models.CASCADE)
    ans = models.JSONField(null=True, default=dict)
    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)
  