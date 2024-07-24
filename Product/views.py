from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from .models import Seller, Ticket,Winner
from PurchasedTicket.models import PurchasedTicket
from UserAccount.models import userAccountModel
from .serializers import TicketSerializer,SellerSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.generics import ListAPIView
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db import transaction
import random
class SaveTicketView(APIView):
    #parser_classes = (MultiPartParser, FormParser)
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
        
class BecomeSellerAPIView(APIView):
    #parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        user_id = request.data.get('user_id')
        image = request.data.get('image')

        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

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
class CheckUserView(APIView):
    def post(self, request, format=None):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        if userAccountModel.objects.filter(id=user_id).exists():
            return Response({'message': 'User is already registered'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
      
## SENDING TICKET OBJECTS
class RetriveTicketList(ListAPIView):
    serializer_class=TicketSerializer
    def get_queryset(self):
        category=self.kwargs['prize_categories']
        return Ticket.objects.filter(prize_categories=category)[:10]
def update_fully_purchased_at(ticket_id):
    # Ensure that ticket_id is a numeric ID
    if isinstance(ticket_id, int):
        ticket = Ticket.objects.get(id=ticket_id)
        purchased_tickets_count = PurchasedTicket.objects.filter(Ticket_id=ticket).count()
        # Convert number_of_tickets to int if it's a string
        if isinstance(ticket.number_of_tickets, str):
            ticket.number_of_tickets = int(ticket.number_of_tickets)
        if purchased_tickets_count == ticket.number_of_tickets:
            ticket.fully_purchased_at = timezone.now()
            ticket.save()
    else:
        raise ValueError("The ticket_id must be a numeric value")
def draw_winner(ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        if not ticket.winner_drawn:
            with transaction.atomic():
                purchased_tickets = PurchasedTicket.objects.filter(Ticket_id=ticket_id)
                if purchased_tickets.exists():
                    winner = random.choice(purchased_tickets)
                    winner_user=winner.User_id 
                    winner_name = winner.User_id.name
                    # print(winner_name)
                    Winner.objects.create(ticket=ticket, winner=winner_user,winner_name=winner_name, Ticket_number=winner)
                    ticket.winner_drawn = True
                    ticket.save()
                    return winner.Ticket_number,winner_name # Return winner's ticket number
    except Ticket.DoesNotExist:
        pass
    return None, None
class SelectWinnerView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            ticket_id = data.get('Ticket_id')

            if ticket_id:
                winner_ticket_number, winner_name = draw_winner(ticket_id)
                if winner_ticket_number:
                    return Response({
                        'status': 'success',
                        'message': 'Winner selected successfully',
                        'winner_ticket_number': winner_ticket_number,
                        'winner_name': winner_name
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'status': 'error',
                        'message': 'Failed to select winner or no purchased tickets found'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'status': 'error',
                    'message': 'Invalid ticket_id'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class SystemSelectWinnerView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            eligible_tickets = Ticket.objects.filter(fully_purchased_at__isnull=False, winner_drawn=False)
            winners = []

            for ticket in eligible_tickets:
                if timezone.now() >= ticket.fully_purchased_at + timezone.timedelta(minutes=5):
                    with transaction.atomic():
                        # Check if winner already exists for this ticket
                        if not Winner.objects.filter(ticket=ticket).exists():
                            winner_ticket_number = draw_winner(ticket.id)
                            if winner_ticket_number:
                                winners.append({'ticket_id': ticket.id, 'winner_ticket_number': winner_ticket_number})
                                ticket.winner_drawn = True
                                ticket.save()

            if winners:
                return Response({'status': 'success', 'message': 'Winners selected successfully', 'winners': winners}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'success', 'message': 'No eligible tickets found'}, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the specific error for debugging purposes
            print(f"Error selecting winners: {e}")
            return Response({'status': 'error', 'message': 'Failed to select winners'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            from rest_framework.views import APIView

class UserTicketsView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = userAccountModel.objects.get(pk=user_id)
        except userAccountModel.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        purchased_tickets = PurchasedTicket.objects.filter(User_id=user)
        
        tickets_data = []
        for purchased_ticket in purchased_tickets:
            ticket_info = {
                'ticket_title': purchased_ticket.Ticket_id.title,
                'ticket_number': purchased_ticket.Ticket_number,
                 'Seller_name':purchased_ticket.Ticket_id.seller.user.name
            }
            tickets_data.append(ticket_info)
        
        return Response(tickets_data)
