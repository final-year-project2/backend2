# serializers.py
from rest_framework import serializers
from Product import models
from PurchasedTicket.models import PurchasedTicket


from django.db.models import Count
from UserAccount.models import userAccountModel
class PichartSerializer(serializers.ModelSerializer):
    category_percentages = serializers.SerializerMethodField()
    class Meta:
        model = models.Ticket
        fields = ['category_percentages']
        
    def get_category_percentages(self, obj):
        # Assuming `obj` is a Seller instance
         tickets = models.Ticket.objects.filter(seller=obj)
         total_campaigns = tickets.count()
         if total_campaigns == 0:
            return []

        # Count the number of campaigns per category
         category_counts = tickets.values('prize_categories').annotate(count=Count('prize_categories'))

        # Convert counts to percentages
         category_percentages = [
            {'category': entry['prize_categories'], 'percentage': (entry['count'] / total_campaigns) * 100}
            for entry in category_counts
         ]

         return category_percentages
class BuyerSerializer(serializers.ModelSerializer):
    # number_of_ticket=serializers.SerializerMethodField()
    class Meta:
        model=userAccountModel
        fields=['name']
        # fields=['name','number_of_ticket']
        
    # def get_number_of_ticket(self,obj):
    #     seller_id=self.kwargs['seller_id']
    #     # all_campaing_by_seller=Ticket.objects.filter(Seller=seller_id)
    #     buyers=PurchasedTicket.objects.filter(ticket__seller__id=seller_id).values('User_id')
    #     buyer_counted=buyers.Count('User_id')
    #     return buyer_counted
      
        