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
from django.http import StreamingHttpResponse
import json
# from sse_wrapper.views import EventStreamView


ticketId=''

class PurchaseTicket(generics.ListCreateAPIView):
    queryset = PurchasedTicket.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
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
            i = 0 
            transaction_from = request.data[i].get('Transaction_from')
            i +=1
            price = ticket_data['Ticket_id'].price_of_ticket
            TotalPrice += int(price)
            ticket_data['User_id'] = user

        if transaction_from=="from_chapa":
            TransactionUpdate(wallet,TotalPrice,transaction_from)
        elif transaction_from == 'from_wallet':
            if wallet.balance >= TotalPrice:
                wallet.balance = wallet.balance-TotalPrice
                wallet.save()
                
                TransactionUpdate(wallet,TotalPrice,transaction_from)
            else:
                return Response({"message":"Your wallet haven't Suficient amount"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"payment type not specified"},status=status.HTTP_400_BAD_REQUEST)
        

        self.perform_create(serializer)
      
    
       
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        qs =  super().get_queryset()
        user = self.request.user
        return qs.filter(User_id = user)

class PurchasedTicketNo(generics.ListAPIView):
    queryset = PurchasedTicket.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PurchasedTicketSerializer
    lookup_field = 'Ticket_id' 
    def get_queryset(self):
        TicketId = self.kwargs['Ticket_id']
        print(TicketId)
        qs =  super().get_queryset()
        return qs.filter(Ticket_id = TicketId)




















# event_queue=[]
# def stream_updates(request):

#     def iterator():
  
#         while True:
#                 ticket = Ticket.objects.get(id=3)
#                 purchased_tickets = PurchasedTicket.objects.filter(Ticket_id= 3)
                
#                 current_count = int(ticket.number_of_tickets) - purchased_tickets.count()
#                 ##NUMBER OF PEOPLE THAT BUT THE TICKET MEAN NUMBER OF USER INSTANCE IN TEH PURCHASED TICKET
#                 unique_buyers_count = PurchasedTicket.objects.filter(Ticket_id=3).values('User_id').distinct().count()

            
#                 event_queue.append(str(current_count))
#                 print(current_count)
                
#                 if event_queue:
#                    event= event_queue.pop(0)
#                    yield f"data:{event, unique_buyers_count}\n\n"
#                 else:
#                     time.sleep(1)
    
#     return StreamingHttpResponse(iterator(),content_type="text/event-stream")
               
                    
        
              
                
                 