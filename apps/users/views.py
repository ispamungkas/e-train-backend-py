import random

from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserSerializer, OTPSerializer, VerifyOTPSerializer, UpdatePasswordSerializer
from .models import User, OTP

d_user = get_user_model()

def is_valid_nip(c_nip):
    
    src = User.objects.all().filter(nip=c_nip)
    
    if len(src) > 0:
        return False
    
    return True

class LoginUserAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    
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
    parser_classes = [FormParser, JSONParser, MultiPartParser]
    
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
  
    ## Create OTP
    def post(self, request):
        otp_serializer = OTPSerializer(data = request.data)
        if otp_serializer.is_valid():
            nip = otp_serializer.validated_data['nip']
            user = User.objects.get(nip=nip)
                
            otp_code = str(random.randint(1000, 9999))
            OTP.objects.create(
                user=user,
                otp_code=otp_code
            )
            
            # Send Code OTP
            subject = "Your OTP was arrived"
            message = f"""Subject: Secure OTP Code for Your Account

Dear {user.name},

For security purposes, please use the One-Time Password (OTP) below to verify your identity:

🔐 Your OTP Code: {otp_code}  
🕒 Validity: 5 minutes  

⚠️ Never share this code with anyone. Our support team will never ask for your OTP.

Best,  
E-Train Security Team
"""
            
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            
            send_mail(subject, message, from_email, recipient_list)
            
            return Response({'message': 'otp code was sended'}, status=status.HTTP_201_CREATED)
        
        error = list(otp_serializer.errors.values())[0][0]
        return Response({'message': error}, status=status.HTTP_400_BAD_REQUEST) 
            
class VerifyOTPAPIView(APIView):
    parser_classes = [FormParser, JSONParser]
    
    def post(self, request):
        verify_serializer = VerifyOTPSerializer(data=request.data)
        if verify_serializer.is_valid():
            otp = verify_serializer.validated_data.get('otp_code')
            
            otp_obj = OTP.objects.filter(otp_code=otp).last()
            
            if otp_obj and otp_obj.is_valid():
                otp_obj.delete()
                return Response({'message': 'otp valid'})
            
            return Response({'message': 'otp_invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
        error = list(verify_serializer.errors.values())[0][0]
        return Response({'message': error}, status=status.HTTP_400_BAD_REQUEST)  
                
class UpdatePasswordAPIView(APIView):
    parser_classes = [FormParser, JSONParser]
    
    def patch(self, request):
        update_serializer = UpdatePasswordSerializer(data=request.data)
        if update_serializer.is_valid():
            nip = update_serializer.validated_data.get('nip')
            new_password = update_serializer.validated_data.get('new_password')
            
            u_obj = User.objects.get(nip=nip)
            u_base = d_user.objects.get(username=nip)
            if not u_obj:
                return Response({'message': 'nip not found'}, status=status.HTTP_404_NOT_FOUND)
            if not u_base:
                return Response({'message': 'nip not found on base'}, status=status.HTTP_404_NOT_FOUND)

            p_hash = make_password(new_password)
            u_obj.password = p_hash
            u_base.set_password(p_hash)
            u_obj.save()
            u_base.save()
            
            return Response({'message': 'password updated'})
        
        error = list(update_serializer.errors.values())[0][0]
        return Response({'message': error}, status=status.HTTP_400_BAD_REQUEST)