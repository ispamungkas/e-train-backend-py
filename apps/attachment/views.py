from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from .serializers import KaryaNyataSerializer, CertificateSerializer, KaryaNyata, QRVerification

class KaryaNyataAPIView(APIView):
    parser_classes = [JSONParser, MultiPartParser,  FormParser]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        param = request.GET.get('id')
        
        k_obj = KaryaNyata.objects.all().order_by('-id')
        if param:
            try:
                k_obj_byid = k_obj.filter(id=param).first()
            except KaryaNyata.DoesNotExist:
                return Response({'message': 'karya nyata not found'}, status=status.HTTP_404_NOT_FOUND)

            k_obj_byid_serialize = KaryaNyataSerializer(k_obj_byid)
            
            return Response({'message': 'karya nyata successfully fetched', 'data': k_obj_byid_serialize.data})
        
        k_serialize = KaryaNyataSerializer(k_obj, many=True)
        return Response({'message': 'karya nyata sucessfully fetched', 'data': k_serialize.data})

    def post(self, request):
        k_serialize = KaryaNyataSerializer(data=request.data)
        
        if k_serialize.is_valid():
            k_serialize.save()
            return Response({'message': 'karya nyata successfully sended'}, status=status.HTTP_201_CREATED)
    
        e_message = list(k_serialize.errors.values())[0][0]
        return Response({'message': k_serialize.error_messages}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        try:
            k_obj = KaryaNyata.objects.get(id=id)
        except KaryaNyata.DoesNotExist:
            return Response({'message': 'karya nyata not found'}, status=status.HTTP_404_NOT_FOUND)
        
        k_serialize = KaryaNyataSerializer(k_obj, data=request.data, partial=True)
        if k_serialize.is_valid():
            k_serialize.save()
            return Response({'message': 'karya nyata successfully updated'}, status=status.HTTP_200_OK)

        e_message = list(k_serialize.errors.values())[0][0]
        return Response({'message': e_message}, status=status.HTTP_400_BAD_REQUEST)

class CertificateAPIView(APIView):
    def post(self, request):
        c_serialize = CertificateSerializer(data = request.data)
        if c_serialize.is_valid():
            c_serialize.save()
            return Response({'message': 'certificate sucessfully created', 'data': c_serialize.data}, status=status.HTTP_201_CREATED)
        
        e_message = list(c_serialize.errors.values())[0][0]
        return Response({'message': e_message}, status=status.HTTP_400_BAD_REQUEST)

class QRVerificationAPIView(APIView):
    def post(self, request):
        data = request.data.get('check')
        q_valid = QRVerification.objects.filter(code=data).first()
        
        if not q_valid:
            return Response({'message': 'certificate not verified'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        return Response({'message': 'certificate verified'})