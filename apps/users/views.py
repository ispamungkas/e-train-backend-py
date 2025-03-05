
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password 
from django.contrib.auth import get_user_model, authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserSerializer
from .models import User

d_user = get_user_model()

def is_valid_nip(c_nip):
    
    src = User.objects.all().filter(nip=c_nip)
    
    if len(src) > 0:
        return False
    
    return True

class LoginUserAPIView(APIView):
    parser_classes = [FormParser]
    
    def post(self, request):
        nip = request.data.get('nip')
        password = request.data.get('password')
        
        ## if the super user has logged
        if nip == 'superuser' and password == 'superuser':
            u_obj = User.objects.get(nip=nip)
            
            ## Checking token for SuperUser
            u_token = authenticate(username=u_obj.nip, password=u_obj.password)
            if u_token:
                refresh = RefreshToken.for_user(u_token)
                u_serialize = UserSerializer(u_obj)
                return Response({'token': str(refresh.access_token), 'message': 'sucessfully login', 'user': u_serialize.data})
            
            return Response({'message': 'invalid credential'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not nip or not password:
            return Response({'message': 'please input require data'}, status=status.HTTP_400_BAD_REQUEST,)
        
        try:
            u_obj = User.objects.get(nip=nip)
        except User.DoesNotExist:
            return Response({'message': 'nip not found'}, status=status.HTTP_404_NOT_FOUND)
           
        ## Checking password
        if not check_password(password=password, encoded=u_obj.password):
            return Response({'message': 'password doesnt match'}, status=status.HTTP_406_NOT_ACCEPTABLE)
         
        u_token = authenticate(username=u_obj.nip, password=u_obj.password)
        if not u_token:
            return Response({'message': 'invalid credential'}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(u_token)
        u_serialize = UserSerializer(u_obj)
        return Response({
            'token': str(refresh.access_token),
            'message': 'successfully login',
            'user': u_serialize.data
        })
        
    def get(self, request):
        
        luser = User.objects.all()
        luser_serialize = UserSerializer(
            luser, many=True
        )
        
        return Response({
            'message': 'user fetched',
            'data': luser_serialize.data
        })
        

# @method_decorator(csrf_exempt, name='dispatch')
class UserAPIView(APIView):
    parser_classes = [FormParser, JSONParser]
    
    def post(self, request):
        if not request.data.get('nip') or not request.data.get('name'):
            return Response({'message': 'please input require data'}, status=status.HTTP_400_BAD_REQUEST,)

        u_serialize = UserSerializer(data=request.data)
        if u_serialize.is_valid():
            u_serialize.save()            
            return Response({'message': 'create account successfully', 'data': u_serialize.data})
        
        erorrs = list(u_serialize.errors.values())[0][0]
        return Response({'message': erorrs}, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateUserAPIVIew(APIView):
    parser_classes = [FormParser,JSONParser, MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, id):
        try:
            u_obj = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'message': 'user not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        u_serialize = UserSerializer(u_obj, data=request.data, partial=True, context={'request': request})
        if u_serialize.is_valid():
            res = u_serialize.save()
            return Response({
                'message': 'user updated',
                'data': UserSerializer(res, context={'request': request}).data
            })
        
        erorrs = list(u_serialize.errors.values())[0][0]
        return Response({'message': erorrs}, status=status.HTTP_400_BAD_REQUEST)

class OTPAPIView(APIView):
    parser_classes = [FormParser, JSONParser]
    
    ## Create Code OTP
    def get(self, request):
        email = request.body.get('email')
        pass
    
    ## Verify Code OTP
    def post(self, request):
        c_otp = request.body.get('otp')
        pass
    
class ForgotPasswordAPIView(APIView):
    parser_classes = [FormParser]
    
    def post(self, request):
        pass