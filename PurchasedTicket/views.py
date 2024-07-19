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
from Product.views import update_fully_purchased_at
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
         # Validate ticket availability
        ticket_counts = {}
        for ticket_data in serializer.validated_data:
            ticket = ticket_data['Ticket_id']
            if ticket.id not in ticket_counts:
                ticket_counts[ticket.id] = 0
            ticket_counts[ticket.id] += 1

        for ticket_id, requested_tickets_count in ticket_counts.items():
            ticket = Ticket.objects.get(id=ticket_id)
            available_tickets_count = int(ticket.number_of_tickets) - PurchasedTicket.objects.filter(Ticket_id=ticket).count()
            if requested_tickets_count > available_tickets_count:
                return Response({
                    "message": f"Not enough tickets available for {ticket}. Requested: {requested_tickets_count}, Available: {available_tickets_count}"
                }, status=status.HTTP_400_BAD_REQUEST)
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
        # After tickets are created, update the fully_purchased_at field if needed
        for ticket_data in serializer.validated_data:
            ticket = ticket_data['Ticket_id']
            update_fully_purchased_at(ticket.id)  # Assuming ticket is an instance of Ticket model

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
    def get_queryset(self):
        qs =  super().get_queryset()
        user = self.request.user
        return qs.filter(User_id = user)







        # transaction = Transaction(
        #     wallet=created,
        #     amount=amount,
        #     transaction_type='withdrawal',
        #     transaction_from = 'from_chapa',# Assuming deposit; change as needed
        #     transaction_date=timezone.now()  # Ensure timezone.now is imported
        # )
        # transaction.save()