
from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Ticket
from .models import Seller
from django.db.models import Count
from PurchasedTicket import models
class TicketSerializer(serializers.ModelSerializer):
    #prize_categories = serializers.JSONField()
    # image_1 = serializers.ImageField(max_length=None, use_url=True, required=False)
    # image_2 = serializers.ImageField(max_length=None, use_url=True, required=False)
    # image_3 = serializers.ImageField(max_length=None, use_url=True, required=False)
    number_of_buyer=serializers.SerializerMethodField()
    ticket_left=serializers.SerializerMethodField()
    

    class Meta:
        model = Ticket
        fields = ['id','seller','title', 'description', 'number_of_tickets','prize_categories','price_of_ticket','image_1','image_2','image_3','number_of_buyer','ticket_left','winner_drawn']
    def get_number_of_buyer(self,obj):
        #   number_of_buyer= models.PurchasedTicket.objects.values('Ticket_id').annotate(unique_buyer=Count('User_id',distinct=True))
          number_of_buyer= models.PurchasedTicket.objects.values('User_id').distinct().count()
          
          
          
          return number_of_buyer
    def get_ticket_left(self,obj):
        purchased_tikcet=models.PurchasedTicket.objects.filter(Ticket_id=obj.id).count()
        numbr_of_ticket=int(Ticket.objects.get(id=obj.id).number_of_tickets)
        ticket_left=numbr_of_ticket-purchased_tikcet
        return ticket_left
        fields = ['id', 'seller','title', 'description', 'number_of_tickets','prize_categories','my_datetime_field','date_createds','price_of_ticket','image_1','image_2','image_3']

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value

    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value

    def validate_number_of_tickets(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value

    def validate_prize_categories(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value


    def validate_image_size(self, image):
        MAX_FILE_SIZE = 10000000 # 10MB
        if image.size > MAX_FILE_SIZE:
            raise ValidationError("File size too big!")
# serializers.py


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['user', 'image', 'successful_campaigns', 'rating']
        
