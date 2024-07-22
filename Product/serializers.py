
from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Ticket
from .models import Seller
from UserAccount.serializer import UserAcountSerializer
class SellerSerializer(serializers.ModelSerializer):
    user = UserAcountSerializer()
    class Meta:
        model = Seller
        fields = ['id','user', 'image', 'successful_campaigns', 'date_created', 'rating']

        
class TicketSerializer(serializers.ModelSerializer):
    seller = SellerSerializer()
    class Meta:
        model = Ticket
        fields = ['id','seller','title', 'description', 'number_of_tickets','prize_categories','price_of_ticket','image_1','image_2','image_3']

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



