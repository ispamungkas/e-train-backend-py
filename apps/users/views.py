import hashlib

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser
from rest_framework import status

from .serializers import UserSerializer
from .models import User

@method_decorator(csrf_exempt, name='dispatch')
class CreateUserAPIView(APIView):
    parser_classes = [FormParser]
    
    def post(self, request):
        nip = request.data.get('nip')
        name = request.data.get('name')
        
        if not nip or not name:
            return Response({'message': 'please input require data'}, status=status.HTTP_400_BAD_REQUEST,)
        
        
        p_hash = make_password(nip)
        u_obj = User.objects.create(
            name=name,
            nip=nip,
            password=p_hash
        )
       
        
        u_serialize = UserSerializer(
            u_obj
        )
        
        return Response({'message': 'create account successfully', 'data': u_serialize.data})