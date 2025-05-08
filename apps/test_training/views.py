from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import PostTest, Answer
from .serializers import PostTestSerializer, AnswerSerializer

class PostTestAPIView(APIView):
    parser_classes = [FormParser, JSONParser]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        param = request.GET.get('id')
        
        if param:
            t_obj = PostTest.objects.get(id=param)
        
            if not t_obj:
                return Response({'message': 'post test not found'}, status=status.HTTP_404_NOT_FOUND)

            t_serialize = PostTestSerializer(t_obj)
            return Response({'message': 'data fetched', 'data': t_serialize.data})
         
        t_obj = PostTest.objects.all()
        t_serialize = PostTestSerializer(t_obj, many=True)
        return Response({'message': 'data fetched', 'data': t_serialize.data})
    
    def post(self, request):
        p_serializer = PostTestSerializer(data=request.data)
        
        if p_serializer.is_valid():
            p_serializer.save()
            return Response({'message': 'post test successfully added'})
            
        e_message = list(p_serializer.errors.values())[0][0]
        return Response({'message': e_message}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        try:
            s_obj = PostTest.objects.get(id=id)
        except:
            return Response({'message': 'post test not exist'}, status=status.HTTP_404_NOT_FOUND)
       
        t_serializer = PostTestSerializer(s_obj, partial=True, data=request.data)
        if t_serializer.is_valid():
            t_serializer.save()
            return Response({'message': 'post test successfully updated', 'data': t_serializer.data}, status=status.HTTP_200_OK)

        e_message = list(t_serializer.errors.values())[0][0]
        return Response({'message': t_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class AnswerAPIView(APIView):
    parser_classes = [FormParser, JSONParser]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        param = request.GET.get('user_id')
        param2 = request.GET.get('post_id')
        
        if param:
            t_obj = Answer.objects.filter(user=param)
        
            if not t_obj:
                return Response({'message': 'post test not found'}, status=status.HTTP_404_NOT_FOUND)

            if param2:
                t_obj = t_obj.filter(post=param2).first()
            
            t_serialize = AnswerSerializer(t_obj)
            return Response({'message': 'data fetched', 'data': t_serialize.data})
         
        t_obj = Answer.objects.all()
        t_serialize = AnswerSerializer(t_obj, many=True)
        return Response({'message': 'data fetched', 'data': t_serialize.data})
    
    def post(self, request):
        a_serializer = AnswerSerializer(data=request.data)
        
        if a_serializer.is_valid():
            a_serializer.save()
            return Response({'message': 'post test successfully added'})
            
        e_message = list(a_serializer.errors.values())[0][0]
        return Response({'message': e_message}, status=status.HTTP_400_BAD_REQUEST)