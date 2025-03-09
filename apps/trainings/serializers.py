import time

from rest_framework import serializers

from .models import Training, Section, Topic, Status
from apps.test_training.serializers import PostTestSerializer

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = (
            'section_id',
            'name',
            'content',
            'img',
            'created_at',
            'updated_at',
            'deleted_at',
        )
        
    def create(self, validated_data):
        s_obj = Topic.objects.create(
            name = validated_data.get('name'),
            section_id = validated_data.get('section_id'),
            content = validated_data.get('content'),
            img = validated_data.get('img')
        )
        
        return s_obj
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.section_id = validated_data.get('section_id', instance.section_id)
        instance.content = validated_data.get('content', instance.content)
        instance.img = validated_data.get('img', instance.img)
        instance.updated_at = time.time()
        instance.save()
        
        return instance
    
class SectionSerializer(serializers.ModelSerializer):
    topics=TopicSerializer(many=True, read_only=True)
    status=serializers.SerializerMethodField()
    
    def get_status(self, obj):
        if obj.topics.all():
            obj.status = Status.COMPLETED
            obj.save()
            return Status.COMPLETED
        return Status.UNCOMPLETED
    
    class Meta:
        model = Section
        fields = (
            'id',
            'name',
            'status',
            'jp',
            'train_id',
            'created_at',
            'updated_at',
            'deleted_at',
            'topics'
        )
        
    def create(self, validated_data):
        s_obj = Section.objects.create(
            name = validated_data.get('name'),
            jp = validated_data.get('jp'),
            train_id = validated_data.get('train_id')
        )
        
        return s_obj
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.jp = validated_data.get('jp', instance.jp)
        instance.updated_at = time.time()
        instance.save()
        
        return instance

class TrainingSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    post_tests = PostTestSerializer(many=True, read_only=True)
    total_jp = serializers.SerializerMethodField()
    is_open = serializers.SerializerMethodField()
    
    def get_total_jp(self, obj):
        return sum(sc.jp for sc in obj.sections.all())
    
    def get_is_open(self, obj):
        if round(time.time()) >= obj.dateline:
            return False
        return True
    
    class Meta:
        model = Training
        fields = (
            'id',
            'name',
            'desc',
            'type_train',
            'type_train_ac',
            'location',
            'link',
            'dateline',
            'total_jp',
            'is_open',
            'is_publish',
            'img',
            'attend',
            'created_at',
            'deleted_at',
            'updated_at',
            'sections',
            'post_tests',
        )
    
    def create(self, validated_data):
        t_obj = Training.objects.create(
            name = validated_data.get('name'),
            desc = validated_data.get('desc'),
            type_train = validated_data.get('type_train'),
            type_train_ac = validated_data.get('type_train_ac'),
            attend = validated_data.get('attend'),
            img = validated_data.get('img'),
            location = validated_data.get('location', None),
            link = validated_data.get('link', None),
            dateline = validated_data.get('dateline'),
        )
        
        return t_obj
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.type_train = validated_data.get('type_train', instance.type_train)
        instance.type_train_ac = validated_data.get('type_train_ac', instance.type_train_ac)
        instance.img = validated_data.get('img', instance.img)
        instance.location = validated_data.get('location', instance.location)
        instance.link = validated_data.get('link', instance.link)
        instance.attend = validated_data.get('attend', instance.attend)
        instance.dateline = validated_data.get('dateline', instance.dateline)
        instance.is_publish = validated_data.get('is_publish', instance.is_publish)
        instance.updated_at = time.time()
        instance.save()
        
        return instance