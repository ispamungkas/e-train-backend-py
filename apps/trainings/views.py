from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from .serializers import TrainingSerializer, SectionSerializer, TopicSerializer
from .models import Training, Section, Topic

# Create your views here.
class TrainingAPIView(APIView):
    parser_classes = [FormParser, JSONParser, MultiPartParser]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        param = request.GET.get('id')
        param2 = request.GET.get('publish')
        
        if param:
            try:
                t_obj = Training.objects.get(id=param)
            except Training.DoesNotExist:
                return Response({'message': 'training not found'}, status=status.HTTP_404_NOT_FOUND)

            t_serialize = TrainingSerializer(t_obj)
            return Response({'message': 'data fetched', 'data': t_serialize.data})
         
        if param2:
            try:
                t_obj = Training.objects.filter(is_publish=True)
            except Training.DoesNotExist:
                return Response({'message': 'training not found'}, status=status.HTTP_404_NOT_FOUND)

            t_serialize = TrainingSerializer(t_obj)
            return Response({'message': 'data fetched', 'data': t_serialize.data})
         
        t_obj = Training.objects.all().order_by('-id')
        t_serialize = TrainingSerializer(t_obj, many=True)
        return Response({'message': 'data fetched', 'data': t_serialize.data})
    
    def post(self, request):
        t_serialize = TrainingSerializer(data = request.data)
        if t_serialize.is_valid():
            t_serialize.save()
            return Response({'message': 'training successfully added', 'data': t_serialize.data}, status=status.HTTP_201_CREATED)
        
        e_message = list(t_serialize.errors.values())[0][0]
        return Response({'message': e_message}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        try:
            s_obj = Training.objects.get(id=id)
        except:
            return Response({'message': 'section not exist'}, status=status.HTTP_404_NOT_FOUND)
       
        t_serializer = TrainingSerializer(s_obj, partial=True, data=request.data)
        if t_serializer.is_valid():
            t_serializer.save()
            return Response({'message': 'section successfully updated', 'data': t_serializer.data}, status=status.HTTP_200_OK)

        e_message = list(t_serializer.errors.values())[0][0]
        return Response({'message': e_message}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        
        try:
            t_obj = Training.objects.get(id=id)
        except:
            return Response({'message': 'training not exist'}, status=status.HTTP_404_NOT_FOUND)
       
        t_obj.soft_delete()
        
        return Response({'message': 'training sucessfully deleted'})
    
class SectionAPIView(APIView):
    parser_classes = [FormParser, JSONParser, MultiPartParser]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        param = request.GET.get('id')
        
        if param:
            try:
                s_obj = Section.objects.get(id=param)
            except Section.DoesNotExist:
                return Response({'message': 'section not found'}, status=status.HTTP_404_NOT_FOUND)
        
            t_serialize = SectionSerializer(s_obj)
            return Response({'message': 'data fetched', 'data': t_serialize.data})
         
        s_obj = Section.objects.all()
        t_serialize = SectionSerializer(s_obj, many=True)
        return Response({'message': 'data fetched', 'data': t_serialize.data})
    
    def post(self, request):
        s_serializer = SectionSerializer(data = request.data)
        if s_serializer.is_valid():
            s_serializer.save()
            return Response({'message': 'section successfully added', 'data': s_serializer.data}, status=status.HTTP_201_CREATED)
        
        e_message = list(s_serializer.errors.values())[0][0]
        return Response({'message': e_message}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        try:
            s_obj = Section.objects.get(id=id)
        except:
            return Response({'message': 'section not exist'}, status=status.HTTP_404_NOT_FOUND)
       
        s_serializer = SectionSerializer(s_obj, partial=True, data=request.data)
        if s_serializer.is_valid():
            s_serializer.save()
            return Response({'message': 'section successfully updated', 'data': s_serializer.data}, status=status.HTTP_200_OK)

        e_message = list(s_serializer.errors.values())[0][0]
        return Response({'message': e_message}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        
        try:
            s_obj = Section.objects.get(id=id)
        except:
            return Response({'message': 'section not exist'}, status=status.HTTP_404_NOT_FOUND)
       
        s_obj.soft_delete()
        return Response({'message': 'section sucessfully deleted'})
    
class TopicAPIView(APIView):
    parser_classes = [FormParser, JSONParser, MultiPartParser]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        param = request.GET.get('id')
        
        if param:
            try:
                t_obj = Topic.objects.get(id=param)
            except Topic.DoesNotExist:                   
                return Response({'message': 'topic not found'}, status=status.HTTP_404_NOT_FOUND)
            
            t_serialize = TopicSerializer(t_obj)
            return Response({'message': 'data fetched', 'data': t_serialize.data})
         
        t_obj = Topic.objects.all()
        t_serialize = TopicSerializer(t_obj, many=True)
        return Response({'message': 'data fetched', 'data': t_serialize.data})
    
    def post(self, request):
        s_serializer = TopicSerializer(data = request.data)
        if s_serializer.is_valid():
            s_serializer.save()
            return Response({'message': 'topic successfully added', 'data': s_serializer.data}, status=status.HTTP_201_CREATED)
        
        e_message = list(s_serializer.errors.values())[0][0]
        return Response({'message': e_message}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        try:
            t_obj = Topic.objects.get(id=id)
        except:
            return Response({'message': 'topic not exist'}, status=status.HTTP_404_NOT_FOUND)
       
        s_serializer = TopicSerializer(t_obj, partial=True, data=request.data)
        if s_serializer.is_valid():
            s_serializer.save()
            return Response({'message': 'topic successfully updated', 'data': s_serializer.data}, status=status.HTTP_200_OK)

        e_message = list(s_serializer.errors.values())[0][0]
        return Response({'message': e_message}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        
        try:
            t_obj = Topic.objects.get(id=id)
        except:
            return Response({'message': 'topic not exist'}, status=status.HTTP_404_NOT_FOUND)
       
        t_obj.soft_delete()
        return Response({'message': 'topic sucessfully deleted'})
    
   