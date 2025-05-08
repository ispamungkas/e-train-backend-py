import time, pytz
from datetime import datetime

from rest_framework import serializers

from .models import KaryaNyata, Certificate, QRVerification

from apps.enrolls.models import Enroll
from apps.users.models import User
from apps.utils.f_utils import create_certificate

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
            enroll = validated_data.get('enroll'), 
            user = validated_data.get('user')
        )
        
        return k_obj
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', KaryaNyata.KaryaNyataStatus.PENDING)
        instance.att = validated_data.get('att', instance.att)
        instance.update_at = time.time()
        instance.save()
        return instance
    

class CertificateSerializer(serializers.ModelSerializer):
    cert = serializers.FileField(required=False)
    enroll = serializers.PrimaryKeyRelatedField(queryset=Enroll.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Certificate
        fields = [
            'id', 'user', 'enroll', 'cert'
        ]
        
    def create(self, validated_data):
        user = validated_data.get('user')
        enroll = validated_data.get('enroll')
        list_section_name = []
        
        for e in enroll.train.sections.all():
            data = [e.name, f'{e.jp}JP']
            list_section_name.append(data)
        
        timezone = pytz.timezone("Asia/Jakarta")
        dt = datetime.fromtimestamp(enroll.train.attend, tz=timezone)

        romawi = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
        month = romawi[dt.month - 1] 
        year = dt.year 
            
        certificate_code = f'{user.id}/TRN-{enroll.train.id}/{enroll.train.name}/{month}/{year}'
        
        QRVerification.objects.create(
            code = certificate_code
        )
        
        file_url = create_certificate(
            train_id= enroll.train.id,
            name=user.name,
            certificate_code = certificate_code,
            train_name= enroll.train.name,
            school= user.c_school,
            listOfSection= list_section_name,
            date= enroll.train.attend
        )
        
        c_obj = Certificate.objects.create(
            user = user,
            enroll = enroll,
            cert = file_url 
        )
        
        return c_obj