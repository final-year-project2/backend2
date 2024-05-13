from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from .models import Seller, Ticket
from .serializers import TicketSerializer
from rest_framework.parsers import MultiPartParser, FormParser
class SaveTicketView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    #permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        # Handle GET request if needed
        return Response({'message': 'GET method is allowed'}, status=status.HTTP_200_OK)
    def post(self, request, format=None):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:    
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# views.py)
class BecomeSellerAPIView(APIView):
    def get(self, request, format=None):
        # Handle GET request if needed
        return Response({'message': 'GET method is allowed'}, status=status.HTTP_200_OK)
    def post(self, request, format=None):
        user_id = request.data.get('user_id')
        if Seller.objects.filter(user_id=user_id).exists():
            return Response({'message': 'User is already registered as a seller'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            seller = Seller.objects.create(user_id=user_id)
            return Response({'message': 'Seller registration successful'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

