
from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Ticket
from .models import Seller
class TicketSerializer(serializers.ModelSerializer):
    #prize_categories = serializers.JSONField()
    # image_1 = serializers.ImageField(max_length=None, use_url=True, required=False)
    # image_2 = serializers.ImageField(max_length=None, use_url=True, required=False)
    # image_3 = serializers.ImageField(max_length=None, use_url=True, required=False)
    class Meta:
        model = Ticket
        fields = ['seller','title', 'description', 'number_of_tickets','prize_categories','image_1','image_2','image_3']

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
class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'
