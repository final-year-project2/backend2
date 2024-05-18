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
class PurchaseTicket(generics.ListCreateAPIView):
    queryset = PurchasedTicket.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PurchasedTicketSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        amount = 0  

        # to get the trandsaction from the request
        transaction_from = request.data[0].get('Transaction_from')
        print(transaction_from)
        for ticket_data in serializer.validated_data:
            # price = ticket_data['Ticket_id'].description
            price = 10
            amount += price
            ticket_data['User_id'] = user
            wallet = get_object_or_404(Wallet, id=user)
            print(wallet.balance)
        WalletOwner, _ = Wallet.objects.get_or_create(user=user)
        if transaction_from == 'from_chapa':
            TransactionUpdate(WalletOwner,amount,transaction_from)
        if transaction_from == 'from_wallet':
            if WalletOwner.balance >= amount:
                WalletOwner.balance = WalletOwner.balance-amount
                Wallet.save()
                TransactionUpdate(WalletOwner,amount,transaction_from)
            else:
                return Response({"message":"Your wallet havent Suficient amount"},status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
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