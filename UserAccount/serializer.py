from rest_framework import serializers
from .models import userAccountModel
from datetime import datetime,timedelta
from django.conf import settings
from twilio.rest import Client
import random
class UserAcountSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only = True,min_length = 6)
    password2 = serializers.CharField(write_only = True,min_length = 6)
    class Meta:
        model = userAccountModel
        fields = [
            'id','name','Email','Phone_no','password1','password2'
        ]
    
    def validate(self, data):
        if data['password1'] !=  data['password2']:
            raise serializers.ValidationError('password do not match')
        return data
    
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
        user.set_password(validated_data['password1'])
        user.save()
        try:
            account_sid = 'AC3b149e8df13637611de9a595d354ca2c'
            auth_token = '1620448415bdf0cc3de4a315a93e568f'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
            body=f'Hello your Otp is {Otp}',
            from_='+13082223702',
            to=f'+251{Phone_no}'
            )
            print(message.sid)
        except:
            print('some thing went ')
        return user