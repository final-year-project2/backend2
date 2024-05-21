from django.utils import timezone
from django.shortcuts import render
from rest_framework import generics,permissions,status
from rest_framework.response import Response
from PurchasedTicket.models import PurchasedTicket
from .serializer import PurchasedTicketSerializer
from UserAccount.models import Wallet,Transaction
from Product.models import Ticket
from .TransactionUpdateMixin import TransactionUpdate
from django.shortcuts import get_object_or_404
from Product.models import Ticket
import time

from sse_wrapper.views import EventStreamView


ticketId=''

class PurchaseTicket(generics.ListCreateAPIView):
    queryset = PurchasedTicket.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PurchasedTicketSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        TotalPrice = 0  
        wallet = get_object_or_404(Wallet, user=user)
        if not wallet:
            return Response({"message":"Wallet dose not exist"},status=status.HTTP_400_BAD_REQUEST)
        
        # to get the trandsaction from the request
        transaction_from = request.data[0].get('Transaction_from')
        print(transaction_from)
        for ticket_data in serializer.validated_data:
            # here to get the price from the database 
            price = ticket_data['Ticket_id'].price_of_ticket
            TotalPrice += int(price)
            ticket_data['User_id'] = user

        if transaction_from == 'from_chapa':
            TransactionUpdate(wallet,TotalPrice,transaction_from)
        if transaction_from == 'from_wallet':
            if wallet.balance >= TotalPrice:
                wallet.balance = wallet.balance-TotalPrice
                wallet.save()
                TransactionUpdate(wallet,TotalPrice,transaction_from)
            else:
                return Response({"message":"Your wallet haven't Suficient amount"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"peyment type not specified"},status=status.HTTP_400_BAD_REQUEST)
        

        self.perform_create(serializer)
        ticket_id=ticket_data['Ticket_id']
        ticketId=ticket_data['Ticket_id']
        number_of_left_tickets= Ticket.objects.get(id=ticket_id)- PurchasedTicket.objects.filter(Ticket_id=ticket_id).count()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_queryset(self):
        qs =  super().get_queryset()
        user = self.request.user
        return qs.filter(User_id = user)





class TicketCountSseView(EventStreamView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ticket_id = kwargs.get('ticket_id')  # Assuming ticket_id is passed as a keyword argument

    def iterator(self):
        last_count = None
        while True:
            try:
                # Optimize by fetching the required data once
                ticket = Ticket.objects.get(id=self.ticket_id)
                purchased_tickets = PurchasedTicket.objects.filter(ticket_id=self.ticket_id)
                
                current_count = ticket.number_of_tickets - purchased_tickets.count()
                
                if current_count!= last_count:
                    yield {
                        "event": "TicketCount",
                        "ticket_left": current_count,
                        "number_of_buyer": purchased_tickets.count(),
                    }
                    last_count = current_count
                
                # Consider using a more efficient method to wait for changes, e.g., via a background task
                time.sleep(1)
            except Exception as e:
                print(f"An error occurred: {e}")
                break  # Exit the loop on error
