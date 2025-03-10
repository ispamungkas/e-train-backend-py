import time

from rest_framework import serializers
from .models import User

from apps.enrolls.serializer import EnrollSerializer

from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

d_user = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    
    ishead = serializers.BooleanField(required=False, write_only=True, default=False)
    enrolls = EnrollSerializer(many=True, read_only=True, fields=['id', 'train', 'status', 'attandence', 'out_date'])

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'nip',
            'email',
            'address',
            'p_number',
            'gender',
            'l_edu',
            'c_school',
            'role',
            'ishead',
            'img_profile',
            'updated_at',
            'created_at',
            'deleted_at',
            'enrolls'
        )
        extra_kwargs = {
            'ishead': {'required': False},
            'img_profile_access': {'required': False}
        }

    def validate_nip(self, value):
        if User.objects.filter(nip=value).exists():
            raise serializers.ValidationError('nip already use')
        return value
    
    def check_role(self, value):
        if value:
            return User.RoleChoice.HEADSCHOOL
        return User.RoleChoice.TEACHER
    
    def create(self, validated_data):
        p_hash = make_password(validated_data['nip'])
        role = validated_data['ishead']
       
        u_obj = User.objects.create(
                name=validated_data['name'],
                nip=validated_data['nip'],
                password=p_hash,
                role=self.check_role(role)
            )
        
        ## Auth register
        d_user.objects.create_user(username=validated_data['nip'], password=p_hash)
        
        return u_obj

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.nip = validated_data.get('nip', instance.nip)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.p_number = validated_data.get('p_number', instance.p_number)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.l_edu = validated_data.get('l_edu', instance.l_edu)
        instance.c_school = validated_data.get('c_school', instance.c_school)
        instance.img_profile = validated_data.get('img_profile', instance.img_profile)
        instance.updated_at = time.time()
        
        instance.save()
        return instance
    
class OTPSerializer(serializers.Serializer):
    nip = serializers.CharField(required=True)
    
    def validate_nip(self, value):
        if not User.objects.filter(nip=value).exists():
            raise serializers.ValidationError('nip not exist') 
        return value
        

class VerifyOTPSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=4, required=True)
    
class UpdatePasswordSerializer(serializers.Serializer):
    nip = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    
