import time

from rest_framework import serializers

from .models import KaryaNyata, Certificate

from apps.enrolls.models import Enroll
from apps.users.models import User

class KaryaNyataSerializer(serializers.ModelSerializer):
    enroll = serializers.PrimaryKeyRelatedField(queryset=Enroll.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = KaryaNyata
        fields = [
           'id', 'att', 'enroll', 'status', 'user'
        ]
        
    def create(self, validated_data):
        k_obj = KaryaNyata.objects.create(
            att = validated_data.get('att'),
            enroll = validated_data.get('enroll')
        )
        
        return k_obj
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', KaryaNyata.KaryaNyataStatus.PENDING)
        instance.ett = validated_data.get('att', instance.att)
        instance.update_at = time.time()
        instance.save()
        return instance
    

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = [
            'id', 'user', 'enroll', 'cert'
        ]
        
    def create(self, request):
        pass