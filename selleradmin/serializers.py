# serializers.py
from rest_framework import serializers
from Product import models

from django.db.models import Count
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