from rest_framework import serializers

from .models import KaryaNyata, Certificate

class KaryaNyataSerializer(serializers.ModelSerializer):
    class Meta:
        model = KaryaNyata
        fields = [
            'att', 'enroll_id', 'status'
        ]

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = [
            'user_id', 'enroll_id', 'cert'
        ]
    