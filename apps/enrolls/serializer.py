
from rest_framework import serializers
from .models import Enroll

from apps.trainings.serializers import TrainingSerializer
from apps.attachment.serializers import Certificate

class EnrollSerializer(serializers.ModelSerializer):
    train_id = TrainingSerializer(read_only=True)
    
    class Meta:
        model = Enroll
        fields = [
            'train_id',
            'user_id',
            'status',
            'out_date',
            'p_learn',
            's_learn',
            'certificate'
        ]

        