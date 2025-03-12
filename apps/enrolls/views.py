from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.response import Response

from .serializer import EnrollSerializer
from .models import Enroll

class EnrollAPIView(APIView):
    parser_classes = [JSONParser, FormParser]
    permission_classes = [IsAuthenticated]
   
    def get(self, request):
        param = request.GET.get('id')
        
        if param:
            try:
                e_obj = Enroll.objects.get(id=param)
            except Enroll.DoesNotExist:
                return Response({'message': 'enroll not found'}, status=status.HTTP_404_NOT_FOUND)
                
            e_serializer = EnrollSerializer(e_obj)
            return Response({'message': 'enroll succesfully fetched', 'data' : e_serializer.data})
        
        e_obj = Enroll.objects.all().order_by('-id')
        e_serializer = EnrollSerializer(e_obj, many=True)
        return Response({'message': 'enroll succesfully fetched', 'data' : e_serializer.data})
        
    def post(self, request):
        e_serializer = EnrollSerializer(data=request.data)
        if e_serializer.is_valid():
            e_serializer.save()
            return Response({'message': 'enroll added successfully'}, status=status.HTTP_201_CREATED)

        e_message = list(e_serializer.errors.values())[0][0]
        return Response({'message': e_message}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, id):
        try:
            e_obj = Enroll.objects.get(id=id)
        except Enroll.DoesNotExist:
            return Response({'message': 'enroll not found'}, status=status.HTTP_404_NOT_FOUND)

        e_serializer = EnrollSerializer(e_obj, data=request.data, partial=True)
        if e_serializer.is_valid():
            e_serializer.save()
            return Response(['message', 'enroll successfully updated'])

        e_message = list(e_serializer.errors.values())[0][0]
        return Response({'message': e_message}, status=status.HTTP_400_BAD_REQUEST)