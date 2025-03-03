from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'name',
            'nip',
            'password',
            'email',
            'address',
            'p_number',
            'gender',
            'l_edu',
            'c_school',
            'role',
            'created_at',
            'deleted_at'
        )