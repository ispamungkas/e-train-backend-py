import time
from rest_framework import serializers

from .models import PostTest, Answer
from apps.users.models import User

class AnswerSerializer(serializers.ModelSerializer):     

    class Meta:
        model = Answer
        fields = [
            'post', 'user', 'ans'
        ]

    def create(self, validated_data):
        p_obj = Answer.objects.create(
            post = validated_data.get('post'),
            ans = validated_data.get('ans'),
            user = validated_data.get('user')
        ) 
        return p_obj

class PostTestSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = PostTest
        fields = [
            'id','train', 'question', 'answers', 'section'
        ]
    
    def create(self, validated_data):
        p_obj = PostTest.objects.create(
            train = validated_data.get('train'),
            question = validated_data.get('question'),
            section = validated_data.get('section')
        ) 
        return p_obj
    
    def update(self, instance, validated_data):
        instance.train = validated_data.get('train', instance.train)
        instance.question = validated_data.get('question', instance.question)
        instance.section = validated_data.get('section', instance.section)
        instance.updated_at = time.time()
        instance.save()
        
        return instance