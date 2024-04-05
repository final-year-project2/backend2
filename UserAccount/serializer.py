from rest_framework import serializers
from .models import userAccountModel
from datetime import datetime,timedelta
from django.conf import settings
from twilio.rest import Client
import random
class UserAcountSerializer(serializers.ModelSerializer):
    # password1 = serializers.CharField(write_only = True,min_length = 6)
    # password2 = serializers.CharField(write_only = True,min_length = 6)
    otp = serializers.CharField(write_only = True , allow_null=True, allow_blank=True)
    class Meta:
        model = userAccountModel
        fields = [
            'id','name','Email','Phone_no','password','otp'
        ]
    
    
    "this create function is used for hash(encript) the password field "
    def create(self, validated_data):
        Otp = random.randint(1000,9999)
        Otp_expre_at = datetime.now() + timedelta(minutes=10)
        Phone_no = int(validated_data['Phone_no']),
        user = userAccountModel(
            name = validated_data['name'],
            Email = validated_data['Email'],
            Phone_no = validated_data['Phone_no'],
            Otp = Otp,
            Otp_expre_at = Otp_expre_at,
            Maximum_otp_try = settings.MAX_OTP_TRY
        )
        user.set_password(validated_data['password'])
        user.save()
        try:
            account_sid = 'ACea49addac6602dcde78dfd3489070132'
            auth_token = '7662fe49f14b65c537775a13675fa48b'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
            body=f'Hello your Otp is {Otp}',
            from_='+13109064102',
            to=f'+251{Phone_no}'
            )
            print(message.sid)
        except:
            print('some thing went wrong try again ')
        return user
from rest_framework import serializers

# class SaveTicketSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=100)
#     description = serializers.CharField(max_length=500)
#     number_of_tickets = serializers.IntegerField()
#     prize_category = serializers.CharField(max_length=100)
#     seller = serializers.CharField(max_length=100) # Adjust the field type as necessary
#     image_1 = serializers.ImageField()
#     image_2 = serializers.ImageField()
#     image_3 = serializers.ImageField()
