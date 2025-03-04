from rest_framework import serializers

from .models import Training, Section, Topic

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        field = (
            'section_id',
            'name',
            'status',
            'content',
            'created_at',
            'deleted_at',
        )

class SectionSerializer(serializers.ModelSerializer):
    topics=TopicSerializer(many=True, read_only=True)
    
    class Meta:
        model = Topic
        field = (
            'name',
            'status',
            'jp',
            'train_id',
            'created_at',
            'deleted_at'
        )

class TrainingSerializer(serializers.ModelSerializer):
    sections=SectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Training
        field = (
            'name',
            'desc',
            'type_train',
            'location',
            'link',
            'date'
            'total_jp',
            'is_open',
            'created_at',
            'deleted_at',
            'sections'
        )