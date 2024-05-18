from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from .models import Seller, Ticket
from .serializers import TicketSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.generics import ListAPIView
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
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, format=None):
        user_id = request.data.get('user_id')
        if user_id is None:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        if Seller.objects.filter(user_id=user_id).exists():
            seller = Seller.objects.get(user_id=user_id)
            return Response({'message': 'User is already registered as a seller', 'seller_id': seller.id}, status=status.HTTP_200_OK)
        
        try:
            seller = Seller.objects.create(user_id=user_id)
            return Response({'message': 'Seller registration successful', 'seller_id': seller.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class RetriveTicketList(ListAPIView):
    queryset=Ticket.objects.all()
    serializer_class=TicketSerializer
    lookup_field='prize_categories'
    
# views.py

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Seller
from .serializers import SellerSerializer
from django.core.exceptions import ObjectDoesNotExist

class BecomeSellerAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        user_id = request.data.get('user_id')
        image = request.data.get('image')

        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_404_BAD_REQUEST)

        try:
            seller = Seller.objects.get(user_id=user_id)
            return Response({
                'message': 'User is already registered as a seller',
                'seller_id': seller.id
            }, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            pass  # User is not already a seller, proceed with registration

        seller_data = {
            'user': user_id,
            'image': image
        }
        serializer = SellerSerializer(data=seller_data)

        if serializer.is_valid():
            seller = serializer.save()
            return Response({
                'message': 'Seller registration successful',
                'seller_id': seller.id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckSellerView(APIView):
    def post(self, request, format=None):
        try:
            user_id = request.data.get('user_id')
            if user_id is None:
                return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            elif Seller.objects.filter(user_id=user_id).exists():
                seller = Seller.objects.get(user_id=user_id)
                return Response({'message': 'User is already registered as a seller', 'seller_id': seller.id}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User is not registered as a seller'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

