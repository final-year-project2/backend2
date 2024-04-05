
from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['seller', 'title', 'description', 'number_of_tickets', 'prize_category', 'image_1', 'image_2', 'image_3']

    def validate_seller(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value

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

    def validate_prize_category(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value

    def validate_image_1(self, value):
        self.validate_image_size(value)
        return value

    def validate_image_2(self, value):
        self.validate_image_size(value)
        return value

    def validate_image_3(self, value):
        self.validate_image_size(value)
        return value

    def validate_image_size(self, image):
        MAX_FILE_SIZE = 10000000 # 10MB
        if image.size > MAX_FILE_SIZE:
            raise ValidationError("File size too big!")
