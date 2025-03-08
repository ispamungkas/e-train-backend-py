from rest_framework import serializers

from .models import KaryaNyata, Certificate
from apps.enrolls.serializer import EnrollSerializer

class KaryaNyataSerializer(serializers.ModelSerializer):
    enroll_id = EnrollSerializer(read_only=True)

    class Meta:
        model = None
        fields = [
            'att', 'enroll_id', 'status'
        ]
        
    @staticmethod
    def get_model(self):
        from apps.attachment.models import KaryaNyata
        return KaryaNyata
    
    def __init__(self, *args, **kwargs):
        self.Meta.model = self.get_model()
        super().__init__(*args, **kwargs)
        

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = [
            'user_id', 'enroll_id', 'cert'
        ]
    