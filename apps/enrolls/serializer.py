import time

from rest_framework import serializers
from .models import Enroll

from apps.trainings.models import Training
from apps.trainings.serializers import TrainingSerializer
from apps.users.models import User

from apps.attachment.serializers import CertificateSerializer, KaryaNyataSerializer

class EnrollSerializer(serializers.ModelSerializer):
    train = serializers.PrimaryKeyRelatedField(queryset=Training.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    certificate = CertificateSerializer(read_only=True, many=True)
    karyanyata = KaryaNyataSerializer(read_only=True, many=True)
    status = serializers.SerializerMethodField()
    out_date = serializers.SerializerMethodField()
    t_jp = serializers.SerializerMethodField()
    training_detail = serializers.SerializerMethodField()
    
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    
    def get_type_train(self, obj):
        return obj.train.type_train
    
    def get_training_detail(self, obj):
        return TrainingSerializer(obj.train, fields=['name', 'desc', 'total_jp', 'dateline', 'location', 'type_train', 'type_train_ac', 'sections', 'attend', 'img']).data
    
    def get_out_date(self, obj):
        if obj.train:
            return obj.train.dateline
        return 0

    def get_t_jp(self, obj):
        return sum(sc.jp for sc in obj.train.sections.all())
    
    def get_status(self, obj):
        if obj.p_learn == 999:
            obj.status = Enroll.Enroll_Status.COMPLETED
            obj.save()
            return Enroll.Enroll_Status.COMPLETED
        
        if 0 < obj.p_learn < 999:

            if time.time() > obj.train.dateline:
                obj.status = Enroll.Enroll_Status.TIMEOUT
                obj.save()
                return Enroll.Enroll_Status.TIMEOUT
            
            return Enroll.Enroll_Status.PROGRESS

        return Enroll.Enroll_Status.NEEDACTION
    
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    
    class Meta:
        model = Enroll
        fields = [
            'id',
            'train',
            'user',
            'status',
            'out_date',
            'p_learn',
            's_learn',
            'attandence',
            'certificate',
            'karyanyata',
            't_jp',
            't_post',
            't_karya_nyata',
            'training_detail',
        ]
        
    def create(self, validated_data):
        e_obj =  Enroll.objects.create(
            user  = validated_data.get('user'),
            train  = validated_data.get('train')
        )
        
        return e_obj
        
    def update(self, instance, validated_data):
        instance.p_learn = validated_data.get('p_learn', instance.p_learn)
        instance.s_learn = validated_data.get('s_learn', instance.s_learn)
        instance.t_post = validated_data.get('t_post', instance.t_post)
        instance.t_karya_nyata = validated_data.get('t_karya_nyata', instance.t_karya_nyata)
        instance.attandence = validated_data.get('attandence', instance.attandence) 
        instance.save()
        
        return instance
        

        