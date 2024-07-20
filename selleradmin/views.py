from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Product.models import Seller,Ticket
from UserAccount.models import userAccountModel
from PurchasedTicket.models import PurchasedTicket
from .serializers import PichartSerializer,BuyerSerializer
from rest_framework import generics,permissions,status
from django.db.models import Count
from django.shortcuts import get_object_or_404
import logging

logger =logging.getLogger(__name__)
class SellerCategoryPercentageAPIView(APIView):
    """
    Retrieve category percentages for a given seller.
    """
    def get_object(self, pk):
        try:
            return Seller.objects.get(pk=pk)
        except Seller.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        seller = self.get_object(pk)
        serializer = PichartSerializer(seller)
        return Response(serializer.data)


# from django.db.models import Count
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import PurchasedTicket, Ticket
# from UserAccount.models import userAccountModel
# from .serializers import UserAcountSerializer  # Ensure this serializer matches your setup

class FrequentBuyer(APIView):
    def get(self, request, seller_id, format=None):
        # Step 1: Find tickets sold by the specific seller
        try:
            seller = Seller.objects.get(id=seller_id)
        except Seller.DoesNotExist:
            return Response({"error": "Seller not found."}, status=404)

        # Step 2: Find all PurchasedTicket entries for tickets sold by this seller
        purchased_tickets = PurchasedTicket.objects.filter(Ticket_id__seller=seller)

        # Extract unique buyer IDs from these purchased tickets
        buyer_ids = purchased_tickets.values_list('User_id', flat=True).distinct()

        # Optionally, annotate each buyer with the count of tickets they've purchased
        buyers_with_counts = PurchasedTicket.objects.filter(User_id__in=buyer_ids).values('User_id').annotate(ticket_count=Count('id'))

        # Convert the queryset to a list of dictionaries for easier processing
        buyers_info = list(buyers_with_counts)

        # Assuming you want to serialize user details, fetch UserAccountModel instances for these buyers
        top_buyer_users = userAccountModel.objects.filter(id__in=buyer_ids)

        # Serialize the user details
        user_serializer = BuyerSerializer(top_buyer_users, many=True)

        # Optionally, attach the count of purchased tickets to each serialized user
        for user_data, buyer_info in zip(user_serializer.data, buyers_info):
            user_data['ticket_count'] = buyer_info['ticket_count']

        return Response(user_serializer.data)
        
        # return top_buyer
        
    
        
        
        
        
#seller may have different ticket sold in the application one ticket may 
# be CAR other may be in electronics category i want for all the ticket sold by that seller id i want to get frequent buyer

#get the seller id //find all the campaign by that seller// find user who is related to that tickets//count the occurance of each related user//
##return 5 of the result.